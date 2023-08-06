try:
    # framework is running
    from .startup_choice import *
except ImportError as _excp:
    # class is imported by itself
    if (
        'attempted relative import with no known parent package' in str(_excp)
        or 'No module named \'omfit_classes\'' in str(_excp)
        or "No module named '__main__.startup_choice'" in str(_excp)
    ):
        from startup_choice import *
    else:
        raise


from omfit_classes.omfit_data import *
from omfit_classes import utils_fusion

try:
    import MDSplus
except Exception as _excp:
    MDSplus = mdsplus_data = None
    warnings.warn('No `MDSplus` support: ' + repr(_excp))
else:
    try:
        # Old versions of MDSplus
        mdsplus_data = MDSplus.data
    except AttributeError:
        # New versions
        mdsplus_data = MDSplus.Data.data

import tqdm
import time
import numpy as np
from uncertainties.unumpy import uarray, std_devs, nominal_values
import weakref

# DIII-D: https://diii-d.gat.com/diii-d/Mdsplusdoc
# NSTX: http://nstx.pppl.gov/nstx/Software/TDI/TDI_GROUPED.HTML
# JET:  http://users.euro-fusion.org/pages/mdsplus/ajc/MDSPLUS.html

__all__ = [
    'OMFITmdsValue',
    'OMFITmds',
    'OMFITmdsObjects',
    'OMFITmdsConnection',
    'MDSplusConnection',
    'translate_MDSserver',
    'tunneled_MDSserver',
    'MDSplus',
    'solveMDSserver',
    'OMFITmdsCache',
    'interpret_signal',
]

D3D_mds_server_trename_selector = {'': 'atlas',
                                   'lbo':'orion'}

# dictionary to translate mnemonic names to MDS+ servers stored in MainSettings['SERVER']
_MDSserverDict = {
    'atlas': 'atlas',
    'atlas.gat.com': 'atlas',
    'orion': 'orion',
    'orion.gat.com': 'orion',
    'DIII-D': D3D_mds_server_trename_selector,
    'gat': D3D_mds_server_trename_selector,
    'D3D': D3D_mds_server_trename_selector,

    'mdsplusdev.gat.com':'mdsplus_dev_gat',

    'jet_mdsplus': 'jet_mdsplus',
    'mdsplus.jet.efda.org': 'jet_mdsplus',
    'jet': 'jet_mdsplus',

    'transpgrid': 'transpgrid',
    'transpgrid.pppl.gov': 'transpgrid',
    'transp': 'transpgrid',

    'skylark': 'skylark',
    'skylark.pppl.gov': 'skylark',
    'pppl': 'skylark',
    'NSTX': 'skylark',

    'mst_mdsplus': 'mst_mdsplus',
    'dave.physics.wisc.edu': 'mst_mdsplus',
    'mst': 'mst_mdsplus',

    'alcdata': 'alcdata',
    'alcdata.psfc.mit.edu': 'alcdata',
    'Alcator': 'alcdata',
    'CMOD': 'alcdata',
    'PSFC': 'alcdata',
    'MIT': 'alcdata',
    'alcdata': 'alcdata',
    'alcdata-new': 'alcdata',

    'tcvdata': 'tcv_mdsplus',
    'tcvdata.epfl.ch': 'tcv_mdsplus',
    'TCV': 'tcv_mdsplus',

    'EAST': 'mds_ipp_ac_cn',

    'EAST_GA': 'eastdata',
    'EAST_US': 'eastdata',

    'KSTAR': 'kstar_mds',
    'kstar_mds': 'kstar_mds',

    'AUG': 'aug_mdsplus',
    'ASDEX': 'aug_mdsplus',
    'aug_mdsplus': 'aug_mdsplus'
}

# from MainSettings['SERVER'] server to MDS+ top tree name
_topLevelMDStreename = {
    'orion': 'D3D',
    'atlas': 'D3D',
    'skylark': 'NSTX',
    'alcdata': 'CMOD',
    'jet_mdsplus': 'JET',
    'eastdata': 'EAST',
    'mds_ipp_ac_cn': 'EAST',
    'mst_mdsplus': 'MST',
    'aug_mdsplus': 'ASDEX',
    'transpgrid': 'TRANSP'
}

my_ip_address = [get_ip()]


def ip_check_reset():
    """reset connections when IP changes, this is necessary to avoid long timeout hardcoded in C part of MDS+"""
    current_ip = get_ip()
    if my_ip_address[0] != current_ip:
        OMFIT.reset_connections()
        printw('Reset SSH connections because IP address has changed from {} to {}.'.format(repr(my_ip_address[0]), repr(current_ip)))
        my_ip_address[0] = current_ip
    return


def translate_MDSserver(server, treename):
    """
    This function maps mnemonic names to real MDS+ servers

    :param server: mnemonic MDS+ name (eg. device name, like DIII-D)

    :param treename: this is to allow selection of a server depending on the treename that is accessed
    """
    if '.' in server:
        if ':' not in server:
            server = server + ':8000'
        return server

    server = utils_fusion.tokamak(server)
    if server.split(':')[0] not in list(OMFIT['MainSettings']['SERVER'].keys()):
        scoreTable = []
        for item in list(_MDSserverDict.keys()):
            m = difflib.SequenceMatcher(None, item.lower(), server.lower())
            match = _MDSserverDict[item]
            if isinstance(match, dict):
                match = match.get(treename, match[''])
            scoreTable.append([m.ratio(), item, match])

        # return best match
        scores = (list(map(eval, np.array(scoreTable)[:, 0])))
        if max(scores) > 0.80:
            server = scoreTable[np.array(scores).argmax()][2]
        else:
            raise OMFITexception("Server '" + server + "' was not recognized.\nYou need to add '" + server + "' to the list of servers in OMFIT['MainSettings']['SERVER']")

    try:
        server = OMFIT['MainSettings']['SERVER'][server]['MDS_server']
    except KeyError:
        pass
    if ':' not in server:
        server = server + ':8000'

    # MDSserver info consists of server with port
    server = ':'.join(parse_server(server)[2:])

    return server


def tunneled_MDSserver(MDSserver, quiet=True, forceRemote=False):
    if ':' not in MDSserver:
        raise ValueError('MDS server `%s` is not in the format hostname:port' % MDSserver)

    # check if ip has changed to avoid long timeout in MDS+ API
    ip_check_reset()

    # all caching is done based on MDSserver0
    MDSserver0 = MDSserver

    # skip this if connection is cached
    if forceRemote or MDSserver0 not in OMFITaux.setdefault('MDSserverReachable', {}):

        # find server in list of supported servers
        username, password, server, port = parse_server(MDSserver, default_username='')
        tunnel = ''
        for item in OMFIT['MainSettings']['SERVER']:
            if isinstance(OMFIT['MainSettings']['SERVER'][item], dict):
                if 'MDS_server' in OMFIT['MainSettings']['SERVER'][item]:
                    if parse_server(OMFIT['MainSettings']['SERVER'][item]['MDS_server'])[2] == server:
                        MDSserver = OMFIT['MainSettings']['SERVER'][item]['MDS_server']
                        tunnel = OMFIT['MainSettings']['SERVER'][item].get('tunnel', '')
                        break

        # if username is provided, then must use MDS+ with SSH protocol
        username, password, server, port = parse_server(MDSserver, default_username='')
        if len(username):
            MDSserver = 'ssh://%s@%s' % (username, server)

        OMFITaux['MDSserverReachable'][MDSserver0] = OMFITmdsConnectionBase(quiet=quiet).test_connection(MDSserver)

        # if direct connection fails, use tunneling
        MDSserver_w_tunnel = MDSserver
        if not OMFITaux['MDSserverReachable'][MDSserver0] and tunnel:
            # handle server tunneling (this function does already buffering)
            username, server, port = setup_ssh_tunnel(assemble_server(username, '', server, port), tunnel, forceTunnel=True, forceRemote=False, allowEmptyServerUsername=True)
            if not len(username):
                MDSserver_w_tunnel = '%s:%s' % (server, port)
            else:
                MDSserver_w_tunnel = 'ssh://%s@%s:%s' % (username, server, port)

        # automatically add ssh-tunneled-servers to _topLevelMDStreename
        _topLevelMDStreename[MDSserver0] = _topLevelMDStreename.get(MDSserver_w_tunnel, MDSserver_w_tunnel)

    return _topLevelMDStreename.get(MDSserver0, MDSserver0)


def MDSplusConnection(server, cached=True, quiet=True):
    '''
    Return a low-level MDSplus.Connection object to the specified MDS+ server
    taking care of establising a tunneled connection if necessary

    :param server: MDS+ server to connect to (also interprets machine names)

    :param cached: whether to return an existing connection to the MDS+ server if one already exists

    :param quiet: verbose or not

    :return: MDSplus.Connection object
    '''
    server0 = translate_MDSserver(server, '')
    tunneled_server = tunneled_MDSserver(server0, quiet=quiet)
    if cached:
        tmp = OMFITmdsConnectionBase(quiet=quiet)
        mds_connection_cache_ID = ('connection', tunneled_server, None, None)
        if mds_connection_cache_ID not in tmp:
            tmp[mds_connection_cache_ID] = MDSplus.Connection(tunneled_server)
        return tmp[mds_connection_cache_ID]
    else:
        return MDSplus.Connection(tunneled_server)


class OMFITmdsObjects(object):
    def __init__(self, server, treename, shot, quiet=True):
        # these are the server, treename and shot exactly as input by the user
        if server in ['None', 'none']:
            server = None
        self.server = server
        if treename in ['None', 'none']:
            treename = None
        self.treename = treename
        if shot in ['None', 'none']:
            shot = None
        if isinstance(shot, str):
            shot = int(shot)
        self.shot = shot

        # self server0, treename0 and shot0 that will be used internally by OMFIT
        # can fail if called when loading a saved mds object prior to the MainSettings server expressions
        # self.interpret_id()

        self.quiet = quiet

    def idConn(self):
        return f'{self.treename} #{self.shot} @ {self.server}'

    def idConnStr(self):
        outstr = ''
        if self.treename:
            outstr += str(self.treename) + ' '
        if self.shot:
            outstr += "#" + str(self.shot) + ' '
        if self.server:
            outstr += "@ " + str(self.server)
        return outstr.strip()

    def interpret_id(self):
        # this function maps the user defined server, treename and shot to the ones that are actually used by by OMFIT

        # handle treename
        treename = self.treename
        if treename is not None:
            try:
                treename = str(evalExpr(treename))
            except Exception:
                pass
            treename = treename.upper()

        # handle shot
        shot = self.shot
        if shot is not None:
            try:
                shot = str(evalExpr(shot))
            except Exception:
                pass

        # server, tree, shot as used in OMFIT
        self.shot0 = shot
        self.treename0 = treename
        self.server0 = translate_MDSserver(self.server, treename)

        return self.server0, self.treename0, self.shot0

    # End of class OMFITmdsObjects


class OMFITmds(SortedDict, OMFITmdsObjects):
    """
    This class returns the structure of an MDS+ tree.
    Objects within this tree are OMFITmdsValue objects

    :param server: string
        MDS+ server or Tokamak device (e.g. `atlas.gat.com` or `DIII-D`)

    :param treename: string
        MDS+ tree

    :param shot: int
        MDS+ shot

    :param subtree: string
        subtree

    :param caching: bool
        OMFITmdsValue use caching system or not

    :param quiet: bool
        print when retrieving data from MDS+
    """

    def __init__(self, server, treename, shot, subtree='', caching=True, quiet=False):
        SortedDict.__init__(self, caseInsensitive=True)
        OMFITmdsObjects.__init__(self, server, treename, shot)
        self.dynaLoad = True
        self.subtree = subtree
        self.caching = caching
        self.quiet = quiet

    @dynaLoad
    def load(self):
        """
        Load the MDS+ tree structure
        """
        # handle ssh connection
        if not hasattr(self, 'server0'):
            self.interpret_id()
        tunneled_server = tunneled_MDSserver(self.server0, quiet=self.quiet)

        # retrieve data structure if id changes
        if not self.quiet:
            printi("Retrieving tree structure from MDS+: " + self.idConnStr())
        tmp = OMFITmdsConnectionBase(quiet=self.quiet).mdsvalue(
            tunneled_server, self.treename0, self.shot0, r'getnci("%s\***","FULLPATH")' % self.subtree
        )

        # traverse all of the tree
        for fullPath in np.atleast_1d(tmp):
            fullTopPath = re.sub(r'(?i)^' + self.treename + "::TOP.", '', b2s(fullPath).lstrip('\\'))
            path = [_f for _f in re.split(':|\\\\|\\.', fullTopPath.strip()) if _f]
            subpath = '\\' + self.treename + "::TOP"
            tr = self
            for sub in path:
                subpath = subpath + '.' + sub
                if sub not in tr:
                    tr[sub] = OMFITmdsValue(server=self.server0, treename=self.treename0, shot=self.shot0, TDI=subpath, caching=self.caching, quiet=self.quiet)
                tr = tr[sub]

        # travel to the subtree
        if self.subtree:
            subtrees = self.subtree.split(':')
            for subtree in subtrees:
                tmp = self[subtree]
                del self[subtree]
                self.update(tmp)

        return

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.__class__.__name__ + '(' + ','.join(map(repr, [self.server, self.treename, self.shot])) + ')'

    def __tree_repr__(self):
        return self.idConnStr(), []

    def __save_kw__(self):
        return {'server': self.server, 'shot': self.shot, 'treename': self.treename, 'subtree': self.subtree, 'caching': self.caching}

    # End of class OMFITmds


_special1 = []


def mds_usage(data):
    if isinstance(data, str):
        return 'text'
    elif isinstance(data, (int, float, np.integer, np.floating)):
        return 'numeric'
    else:
        return 'signal'


class OMFITmdsConnection(object):
    """
    This class that provides a convenient interface to the OMFITmdsConnectionBaseClass
    Specifically it allows specifiying series of commands (mdsvalue, write, write_dataset, tcl, test_connection)
    without having to re-type the server for each command.
    """

    def __init__(self, server, *args, **kw):
        server0 = translate_MDSserver(server, '')
        self.tunneled_server = tunneled_MDSserver(server0, quiet=kw.get('quiet', True))
        self.OMFITmdsConnectionBase = OMFITmdsConnectionBase(*args, **kw)

    def mdsvalue(self, treename, shot, what, timeout=None):
        return self.OMFITmdsConnectionBase.mdsvalue(server=self.tunneled_server, treename=treename, shot=shot, what=what, timeout=timeout)


    def write(self, treename, shot, node, data, error=None, units=None):
        return self.OMFITmdsConnectionBase.write(server=self.tunneled_server, treename=treename, shot=shot, node=node, data=data, error=error, units=units)

    def write_dataset(self, treename, shot, subtree, xarray_dataset, quantities=None, translator=None):
        return self.OMFITmdsConnectionBase.write_dataset(server=self.tunneled_server, treename=treename, shot=shot, subtree=subtree, xarray_dataset=xarray_dataset, quantities=quantities, translator=translator)

    def create_model_tree(self, treename, subtree, data, clear_subtree=False):
        return self.OMFITmdsConnectionBase.create_model_tree(server=self.tunneled_server, treename=treename, subtree=subtree, data=data, clear_subtree=clear_subtree)

    def tcl(self, tcl):
        return self.OMFITmdsConnectionBase.tcl(server=self.tunneled_server, tcl=tcl)

    def test_connection(self):
        return self.OMFITmdsConnectionBase.test_connection(server=self.tunneled_server)

    # End of class OMFITmdsConnection


class OMFITmdsConnectionBaseClass(SortedDict):
    """
    This class handles the low-level connection to a MDS+ server
    Internally the class makes use of a caching system to reuse connections that are already open
    NOTE: do not use this class directly, instead make use of OMFITmdsConnectionBase,
          which can safely handle MDS+ connections in parallel processes.
    """

    def __init__(self, quiet=True, timeout=-1):
        """
        :param quiet: bool
            Suppresses some informational print statements about MDSplus connections being opened / used / checked

        :param timeout: int
            Timeout setting passed to MDSplus.Connection.get(), in ms. -1 seems to disable timeout.
            Only works for newer MDSplus versions, such as 7.84.8.
        """
        SortedDict.__init__(self, limit=100)
        self.quiet = quiet
        if compare_version(getattr(MDSplus,'__version__','0.0.0'), '7.84.0') < 0 and timeout != -1:
            printw(
                'WARNING: Older versions of MDSplus ignore the timeout keyword. Your setting of {} ms probably will '
                'not be respected by MDSplus version {}'.format(timeout, getattr(MDSplus,'__version__','0.0.0'))
            )
        self.timeout = timeout

    def mdsvalue(self, server, treename, shot, what, timeout=None):
        timeout = self.timeout if timeout is None else timeout

        tmp = re.findall('[\'"].*[\'"]', what)
        if len(tmp) and '\\' not in what and '(' not in what:
            signal = tmp[0]
            pre, post = what.split(signal)
            signal = tmp[0].strip('\'"')
        elif '=' in what:
            try:
                pre, signal = what.split('=')
                pre = pre + '='
                post = ''
            except ValueError:
                signal = what
                pre = ''
                post = ''
        else:
            signal = what
            pre = ''
            post = ''

        mds_connection_cache_ID = ('read', server, treename, shot)

        # try twice, the second time reconnect to server
        for fallback in range(2):

            try:

                if fallback or mds_connection_cache_ID not in self:
                    if fallback:
                        printi('* Re-connecting to: ' + server)
                        time.sleep(np.random.rand())
                    printd('* Connecting to: ' + server, topic='MDS')
                    self[mds_connection_cache_ID] = MDSplus.Connection(server)

                if treename is None and shot is not None:
                    try:
                        signal = b2s(self[mds_connection_cache_ID].get('findsig("' + signal + '",_fstree)', timeout=timeout).value)
                        treename = self[mds_connection_cache_ID].get('_fstree', timeout=timeout).value
                    except Exception:
                        pass

                if what is not None:
                    if shot is not None:
                        if treename is not None:
                            self[mds_connection_cache_ID].openTree(treename, int(shot))
                            try:
                                queryResult = mdsplus_data(self[mds_connection_cache_ID].get(pre + signal + post, timeout=timeout))
                                printd(f'* Retrieving data {treename} for shot {shot}', topic='MDS')
                            except MDSplus.MdsException as _excp:
                                if 'Node Not Found' in repr(_excp):
                                    return _special1
                                elif 'No data available for this node' in repr(_excp):
                                    return _special1
                                else:
                                    raise
                        else:
                            try:
                                queryResult = mdsplus_data(self[mds_connection_cache_ID].get(what, timeout=timeout))
                                printd('* Retrieving data signal', topic='MDS')
                            except Exception as _excp:
                                printd(repr(_excp), topic='MDS')

                                if 'jet' in server:
                                    if '@' not in signal:
                                        signal = 'jetppf@' + signal
                                    directory, signal = signal.split('@')
                                    queryResult = mdsplus_data(self[mds_connection_cache_ID].get('ppfuid("' + directory + '");' + pre + 'jet("' + signal + '",' + shot + ')' + post, timeout=timeout))
                                    printd('* Retrieving data ' + pre + 'jet("' + signal + '",' + shot + ')' + post, topic='MDS')
                                else:
                                    try:
                                        try:
                                            queryResult = mdsplus_data(self[mds_connection_cache_ID].get(pre + 'ptdata2("' + signal + '",' + shot + ')' + post, timeout=timeout))
                                            if queryResult is not None and len(queryResult)==1 and queryResult[0]==0:
                                                raise Exception('Try local PTDATA')
                                            printd('* Retrieving remote data ' + pre + 'ptdata2("' + signal + '",' + shot + ')' + post, topic='MDS')
                                        except Exception as _excp:
                                            try:
                                                queryResult = mdsplus_data(MDSplus.TdiExecute(pre + 'ptdata2("' + signal + '",' + shot + ')' + post))
                                                printd('* Retrieving local data ' + pre + 'ptdata2("' + signal + '",' + shot + ')' + post, topic='MDS')
                                            except Exception:
                                                if 'Try local PTDATA' in repr(_excp):
                                                    pass
                                                else:
                                                    raise _excp

                                    except Exception as _excp:
                                        printd(repr(_excp), topic='MDS')
                                        try:
                                            queryResult = mdsplus_data(self[mds_connection_cache_ID].get(pre + 'pseudo("' + signal + '",' + shot + ')' + post, timeout=timeout))
                                            printd('* Retrieving data ' + pre + 'pseudo("' + signal + '",' + shot + ')' + post, topic='MDS')
                                        except Exception as _excp:
                                            printd(repr(_excp), topic='MDS')
                                            raise MDSplus.MdsException('Failed to retrieve data from PTDATA: server=`%s` shot=`%s` what=`%s` [ %s ]' % (server, shot, what, repr(_excp)))
                    else:
                        try:
                            printd('* ' + what, topic='MDS')
                            try:
                                queryResult = mdsplus_data(self[mds_connection_cache_ID].get(what, timeout=timeout))
                                if queryResult is not None and len(queryResult)==1 and queryResult[0]==0:
                                    raise Exception('Try local PTDATA')
                            except Exception as _excp:
                                try:
                                    queryResult = mdsplus_data(MDSplus.TdiExecute(what))
                                except Exception:
                                    if 'Try local PTDATA' in repr(_excp):
                                        pass
                                    else:
                                        raise _excp
                        except Exception:
                            raise MDSplus.MdsException('Failed to execute operation: server=`%s` treename=`%s` what=`%s`' % (server, treename, what))

                    printd('* Querying ' + what + "  ->  " + str(type(queryResult)), topic='MDS')

                    return queryResult

                else:
                    return None

                break  # fallback loop

            except MDSplus.MdsException as _excp:
                if fallback:
                    raise

    def write(self, server, treename, shot, node, data, error=None, units=None):
        '''
        Write the data to MDS+

        :param server: The MDS+ server

        :param treename: The MDS+ tree

        :param shot: The pulse number of the tree to write to

        :param subtree: The location in the tree to write to

        :param data: data to be written.
                     If an xarray.DataArray its dimensions and units will also be written

        :param error: error to be written (ignored if data is DataArray)

        :param units: units to be written (ignored if data is DataArray)

        :param quantities: list of quantities to write
        '''
        mds_connection_cache_ID = ('write', server, treename, shot)
        if mds_connection_cache_ID not in self:
            self[mds_connection_cache_ID] = MDSplus.Connection(server)
            self[mds_connection_cache_ID].openTree(treename, shot)
        conn = self[mds_connection_cache_ID]

        # generate TDI expression for writing data to MDS+
        text = []
        arg = []
        if isinstance(data, xarray.DataArray):
            for var in [''] + reversed(list(data.dims)):  # reversed so default plotting (double-click) in OMFIT GUI works
                item = data[var]
                txt = '$'
                if 'units' in item.attrs:
                    txt = 'build_with_units(%s,%s)' % (txt, item.attrs['units'])
                if is_uncertain(item.values):
                    txt = 'build_with_error(%s,%s)' % (txt, txt)
                    arg.extend([nominal_values(item.values), std_devs(item.values)])
                else:
                    arg.append(item.values)
                text.append(txt)
            txt = 'make_signal(%s,*,%s)' % (text[0], ','.join(text[1:]))
        else:
            txt = '$'
            if units:
                txt = 'build_with_units(%s,"%s")' % (txt, units)
            if error:
                txt = 'build_with_error(%s,%s)' % (txt, txt)
                arg.extend([data, error])
            else:
                arg.append(data)
        try:
            conn.put(node, txt, *arg)
        except Exception as _excp:
            raise _excp.__class__(f'\n{node} {txt}\n' + str(_excp))

    def write_dataset(self, server, treename, shot, subtree, xarray_dataset, quantities=None, translator=None):
        '''
        Write the contents of xarray_dataset to MDS+, with smart referencing of dimensions

        :param server: The MDS+ server

        :param treename: The MDS+ tree

        :param shot: The pulse number of the tree to write to

        :param subtree: The location in the tree to write to

        :param xarray_dataset: An xarray Dataset to write to subtree

        :param quantities: list of quantities to write

        :param translator: a function that translates nodes from their dataset value to a string shorter than 12 chars
        '''
        if translator is None:
            translator = lambda x:x

        mds_connection_cache_ID = ('write', server, treename, shot)
        if mds_connection_cache_ID not in self:
            self[mds_connection_cache_ID] = MDSplus.Connection(server)
            # create pulse from model tree
            self[mds_connection_cache_ID].get(f"tcl('set tree {treename}')")
            self[mds_connection_cache_ID].get(f"tcl('create pulse {shot}')")
            self[mds_connection_cache_ID].get(f"tcl('write')")
            self[mds_connection_cache_ID].get(f"tcl('close')")
            # open tree
            self[mds_connection_cache_ID].openTree(treename, shot)
            if subtree:
                self[mds_connection_cache_ID].setDefault(subtree)
        conn = self[mds_connection_cache_ID]

        # subselect list of quantities from dims
        dim_quantities = list(xarray_dataset.dims.keys())
        if quantities is not None:
            dim_quantities = [k for k in dim_quantities if k in quantities]
        # assign dimensions
        for dim in tqdm.tqdm(dim_quantities, file=sys.stdout):
            item = xarray_dataset[dim]
            arg = []
            txt = '$'
            if 'units' in item.attrs:
                txt = 'build_with_units(%s,"%s")' % (txt, item.attrs['units'])
            if is_uncertain(item.values):
                txt = 'build_with_error(%s,%s)' % (txt, txt)
                arg.extend([nominal_values(item.values), std_devs(item.values)])
            else:
                arg.append(item.values)
            try:
                conn.put(f'{translator(dim)}', txt, *arg)
            except Exception as _excp:
                raise _excp.__class__(f'\n\\{dim} {txt}\n' + str(_excp))

        # subselect list of quantities from variables
        var_quantities = list(xarray_dataset.data_vars.keys())
        if quantities is not None:
            var_quantities = [k for k in var_quantities if k in quantities]
        # assign variables
        for var in tqdm.tqdm(var_quantities, file=sys.stdout):
            item = xarray_dataset[var]
            arg = []
            txt = '$'
            if 'units' in item.attrs:
                txt = 'build_with_units(%s,"%s")' % (txt, item.attrs['units'])
            if is_uncertain(item.values):
                txt = 'build_with_error(%s,%s)' % (txt, txt)
                arg.extend([nominal_values(item.values), std_devs(item.values)])
            else:
                arg.append(item.values)
            txt = 'make_signal(%s,*,%s)' % (txt, ','.join([translator(dim) for dim in reversed(item.dims)]))
            try:
                conn.put(f'{translator(var)}', txt, *arg)
            except Exception as _excp:
                raise _excp.__class__(f'\n\\{var} {txt}\n' + str(_excp))
        return dim_quantities + var_quantities

    def create_model_tree(self, server, treename, subtree, data, clear_subtree=False):
        '''
        Create new nodes OMFIT.subtree.<data.keys()> on server

        :param server: The MDS+ server (OMFIT serverish)

        :param treename: In which MDS+ tree to create the model trees

        :param subtree: The string describing the code or workflow, e.g. "ONETWO" (less than twelve characters)

        :param clear_subtree: Whether to clear the subtree node
        '''
        if len(treename) > 12:
            raise ValueError('MDS+ treename can only be 12 characters long: ' + treename)
        if len(subtree) > 12:
            raise ValueError('MDS+ path parts can only be 12 characters long: ' + subtree)

        def traverse(me, path):
            if isinstance(me, Dataset) or isinstance(me, OMFITdataset):
                kids = me.variables
            elif isinstance(me, dict):
                kids = me.keys()
            path.append(None)
            for kid in tqdm.tqdm(kids, file=sys.stdout):
                path[-1] = kid
                # is deleting of the nodes necessary?
                # tcl = f"delete node {'.'.join(path)} /confirm"
                # self.tcl(server, tcl)
                tcl = f"add node {'.'.join(path)} /usage={mds_usage(me[kid])}"
                self.tcl(server, tcl)

                if isinstance(me[kid], dict):
                    traverse(me[kid], copy.deepcopy(path))

        self.tcl(server, f'edit {treename}/shot=-1')
        if subtree:
            if clear_subtree:
                self.tcl(server, f'delete node {subtree} /confirm')
            self.tcl(server, f'add node {subtree} /usage=structure')
            traverse(data, [subtree])
        else:
            traverse(data, [])

        self.tcl(server, 'write')
        self.tcl(server, 'close')

    def tcl(self, server, tcl):
        mds_connection_cache_ID = ('tcl', server, None, None)

        # try twice, the second time reconnect to server
        for fallback in range(2):

            try:
                if fallback or mds_connection_cache_ID not in self:
                    if fallback:
                        printi('* Re-connecting to: ' + server)
                    printd('* Connecting to: ' + server, topic='MDS')
                    self[mds_connection_cache_ID] = MDSplus.Connection(server)

                return self[mds_connection_cache_ID].get("tcl(" + repr(tcl) + ")")

            except MDSplus.MdsException as _excp:
                if fallback:
                    raise

    def test_connection(self, test_server):
        username, password, server, port = parse_server(test_server)
        if test_connection(username, server, port):
            try:
                MDSplus.Connection(test_server)
                return True
            except Exception as _excp:
                if 'Error connecting to' in str(_excp):
                    return False
                else:
                    raise
        return False

_OMFITmdsConnectionBaseObjects = {}


def OMFITmdsConnectionBase(*args, **kw):
    '''
    returns OMFITmdsConnectionBaseClass objects, in a way that is safe for each parallel process
    '''
    tmp = '_'.join(map(str, OMFITaux.setdefault('prun_process', [])))
    if tmp not in _OMFITmdsConnectionBaseObjects:
        _OMFITmdsConnectionBaseObjects[tmp] = OMFITmdsConnectionBaseClass(*args, **kw)
    return _OMFITmdsConnectionBaseObjects[tmp]


class OMFITcaching(SortedDict):
    def __init__(self, type, cachesDir=True, limit=1000):
        '''
        :param type: string with cache type

        :param cachesDir: directory to use for off-line storage of data
                          If `True` it defaults to OMFIT['MainSettings']['SETUP']['cachesDir']
                          If `False`, then off-line caching is disabled
                          If a string, then that value is used

        :param limit: limit number of elements for in-memory caching
        '''
        SortedDict.__init__(self, limit=limit)
        self._cachesDir = cachesDir
        self.type = type

    def __getitem__(self, key):
        if key in self:
            return b2s(SortedDict.__getitem__(self, key))
        else:
            cachesDir = self.cachesDir
            if cachesDir:
                directory, filename = os.path.split(os.sep.join([cachesDir] + list(map(str, key))))
                filename = omfit_hash(filename,10) + '.pkl'
                if os.path.exists(directory + os.sep + filename):
                    try:
                        with open(directory + os.sep + filename, 'rb') as f:
                            value = pickle.load(f)
                    except Exception:
                        os.remove(directory + os.sep + filename)
                        raise KeyError('%s cache error: %s' % (self.type, key,))
                    SortedDict.__setitem__(self, key, b2s(value))
                    return b2s(value)
                raise KeyError('%s cache miss: %s' % (self.type, key,))
            else:
                raise KeyError('%s cache miss: %s' % (self.type, key,))

    def __setitem__(self, key, value):
        cachesDir = self.cachesDir
        if cachesDir:
            directory, filename = os.path.split(os.sep.join([cachesDir] + list(map(str, key))))
            filename = omfit_hash(filename,10) + '.pkl'
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                except FileExistsError:
                    pass
            with open(directory + os.sep + filename, 'wb') as f:
                pickle.dump(value, f)
        SortedDict.__setitem__(self, key, b2s(value))
        return b2s(value)

    @property
    def cachesDir(self):
        if self._cachesDir is True:
            cachesDir = OMFIT['MainSettings']['SETUP'].get('cache_directory', False)
            if cachesDir is True:
                cachesDir = locals().get('OMFITglobaltmpDir', '/tmp/' + os.environ.get('USER', 'user')) + '/OMFITcache/'
            elif cachesDir and not isinstance(cachesDir, str):
                raise Exception("OMFIT['MainSettings']['SETUP']['MDS_cache_dir'] can only be a string with a directory or `True` or `False`")
        else:
            cachesDir = self._cachesDir
        if cachesDir:
            return os.path.abspath(cachesDir + os.sep + self.type)

    def purge(self):
        self.clear()
        cachesDir = self.cachesDir
        if cachesDir and os.path.exists(cachesDir):
            shutil.rmtree(cachesDir, ignore_errors=True)

    def __popup_menu__(self):
        return [['Purge %s cache' % self.type, self.purge], ]

    # End of class OMFITcaching


__HDD_MDS_cache__ = OMFITcaching(type='MDS')


def OMFITmdsCache(cachesDir=_special1, limit=_special1):
    """
    Utility function to manage OMFIT MDS+ cache

    :param cachesDir: directory to use for off-line storage of data
                      If `True` it defaults to OMFIT['MainSettings']['SETUP']['cachesDir']
                      If `False`, then off-line MDS+ caching is disabled
                      If a string, then that value is used

    :param limit: limit number of elements for in-memory caching

    NOTE: off-line caching can be achieved via:

    >> # off-line caching controlled by OMFIT['MainSettings']['SETUP']['cachesDir']
    >> OMFIT['MainSettings']['SETUP']['cachesDir'] = '/path/to/where/MDS/cache/data/resides'
    >> OMFITmdsCache(cachesDir=True)
    >>
    >> # off-line caching for this OMFIT session to specific folder
    >> OMFITmdsCache(cachesDir='/path/to/where/MDS/cache/data/resides')
    >>
    >> # purge off-line caching (clears directory based on `cachesDir`)
    >> OMFITmdsCache().purge()
    >>
    >> # disable off-line caching for this OMFIT session
    >> OMFITmdsCache(cachesDir=False)
    >>
    >> # disable default off-line caching
    >> OMFIT['MainSettings']['SETUP']['cachesDir']=False
    """
    if cachesDir is not _special1:
        __HDD_MDS_cache__._cachesDir = cachesDir
    if limit is not _special1:
        __HDD_MDS_cache__.limit = limit
    return __HDD_MDS_cache__


class OMFITmdsValue(dict, OMFITmdsObjects):
    r"""
    This class provides access to MDS+ value and allows execution of any TDI commands.
    The MDS+ value data, dim_of units, error can be accessed by the methods defined in this class.
    This class is capable of ssh-tunneling if necessary to reach the MDSplus server.
    Tunneling is set based on OMFIT['MainSettings']['SERVER']

    :param server: MDS+ server or Tokamak device (e.g. `atlas.gat.com` or `DIII-D`)

    :param treename: MDS+ tree (None or string)

    :param shot: MDS+ shot (integer or string)

    :param TDI: TDI command to be executed

    :param quiet: print if no data is found

    :param caching: if False turns off caching system, else behaviour is set by OMFITmdsCache

    :param timeout: int
        Timeout setting passed to MDSplus.Connection.get(), in ms. -1 seems to disable timeout.
        Only works for newer MDSplus versions, such as 7.84.8.

    >> tmp=OMFITmdsValue(server='DIII-D', treename='ELECTRONS', shot=145419, TDI='\\ELECTRONS::TOP.PROFILE_FITS.ZIPFIT.EDENSFIT')
    >> x=tmp.dim_of(0)
    >> y=tmp.data()
    >> pyplot.plot(x,y.T)

    To resample data on the server side, which can be much faster when dealing with large data and slow connections,
    provide t_start, t_end, and dt in the system's time units (ms or s). For example, to get stored energy from EFIT01
    from 0 to 5000 ms at 50 ms intervals (DIII-D uses time units of ms; some other facilities like KSTAR use seconds):

    >> wmhd = OMFITmdsValue(server='DIII-D', shot=154749, treename='EFIT01', TDI=r'resample(\WMHD, 0, 5000, 50)')

    The default resample function uses linear interpolation. To override it and use a different method, see
    http://www.mdsplus.org/index.php/Documentation:Users:LongPulseExtensions#Overriding_Re-sampling_Procedures

    To access DIII-D PTDATA, set `treename=None` and use the `TDI` keyword to pass signal to be retrieved.
    Note: PTDATA `ical` option can be passed by setting the `shot` keyword as a string with the shot number followed by the ical option separated by comma. e.g. shot='145419,1'

    >> tmp=OMFITmdsValue('DIII-D', treename=None, shot=145419, TDI='ip')
    >> x=tmp.dim_of(0)
    >> y=tmp.data()
    >> pyplot.plot(x,y)
    """

    def __init__(self, server, treename=None, shot=None, TDI=None, quiet=False, caching=True, timeout=-1):
        dict.__init__(self)

        OMFITmdsObjects.__init__(self, server, treename, shot)

        self.TDI = TDI
        self.quiet = quiet
        self.caching = caching
        self.timeout = timeout
        if compare_version(getattr(MDSplus,'__version__','0.0.0'), '7.84.0') < 0 and timeout != -1:
            printw(
                'WARNING: Older versions of MDSplus ignore the timeout keyword. Your setting of {} ms probably will '
                'not be respected by MDSplus version {}'.format(timeout, getattr(MDSplus,'__version__','0.0.0'))
            )

    # DATA (can be overridden by subclassing --> _base_data)
    def data(self):
        '''
        :return: array with the data
        '''
        return self._base_data()

    def _base_data(self):
        self._fetch_data()
        if not hasattr(self, '_data') or self._data is _special1:
            return
        return copy.deepcopy(self._data)

    # DIM_OF
    def dim_of(self, index):
        """
        :param index: index of the dimension

        :return: array with the dimension of the MDS+ data for its dimension `index`
        """
        self._fetch_dim_of()
        if not hasattr(self, '_data') or self._data is _special1:
            return
        return copy.deepcopy(self._dim_of.get(int(index), None))

    # UNITS
    def units(self):
        """
        :return: string of the units of the MDS+ data
        """
        self._fetch_units()
        if not hasattr(self, '_data') or self._data is _special1:
            return
        return copy.deepcopy(self._units)

    # UNITS_DIM_OF
    def units_dim_of(self, index):
        """
        :param index: : index of the dimension
        :return: string of the units of the MDS+ dimension `index`
        """
        self._fetch_units_dim_of()
        if not hasattr(self, '_data') or self._data is _special1:
            return
        return copy.deepcopy(self._units_dim_of.get(int(index), None))

    # ERROR (can be overridden by subclassing --> _base_error)
    def error(self):
        '''
        :return: array with the error
        '''
        return self._base_error()

    def _base_error(self):
        self._fetch_error()
        if not hasattr(self, '_data') or self._data is _special1:
            return
        return copy.deepcopy(self._error)

    # ERROR_DIM_OF
    def error_dim_of(self, index):
        """
        :param index: index of the dimension

        :return: array with the dimension of the MDS+ error for its dimension `index`
        """
        self._fetch_error_dim_of()
        if not hasattr(self, '_data') or self._data is _special1:
            return
        return copy.deepcopy(self._error_dim_of.get(int(index), None))

    # XARRAY DATA
    def xarray(self):
        '''
        :return: DataArray with information from this node
        '''

        if not self.check():
            raise ValueError('No data in %s on %s' % (self.TDI, self.idConnStr()))

        data = self.data()
        e = self.error()
        if e is not None and e.size and b2s(e[0]) != '':
            data = uarray(data, np.abs(e))
        dims = ['dim_%d' % k for k in range(data.ndim)]
        clist=[]
        elist=[]
        evalid=[]

        for k, c in enumerate(dims):
            clist.append(self.dim_of(k))
            e = self.error_dim_of(k)
            if e and len(e) and e[0] != '':
                clist[k] = uarray(clist[k], np.abs(e))
                elist.append(e)
            else:
                elist.append(np.zeros(np.shape(clist[k])))

        # this is meant to fix order of the dims array to match the order dimensions of the data array,
        # which can be reversed because of the MDSplus package implementation.
        # it can handle the case where any dimension array is actually multidimensional (with the same shape as the data array)

        idims = np.arange(len(dims))
        if data.shape != tuple([len(k) if np.ndim(k) == 1 else k.shape[ik] for ik, k in enumerate(clist)]):
            dims = dims[::-1]
            idims = idims[::-1]
            clist = clist[::-1]
            elist = elist[::-1]
            evalid = evalid[::-1]

        coords = {}
        for index, dim, arr in zip(idims, dims, clist):
            if np.ndim(arr) == 1:
                ck = dim
                coords[dim] = ([dim], arr, {'units': self.units_dim_of(index)})
            else:
                coords[dim + '_val'] = (dims, arr, {'units': self.units_dim_of(index)})

        xdata = DataArray(data, dims=dims, coords=coords, attrs={'units': self.units()})
        return xdata

    @property
    def MDSconn(self):
        # The .MDSconn attribute establishes a MDS+ connection (if not already connected) and returns it
        # NOTE: use of weakrefs is necessary for deepcopying OMFITmdsValue objects
        if not hasattr(self, '_MDSconn') or self._MDSconn() is None:
            self._MDSconn = weakref.ref(OMFITmdsConnectionBase(quiet=self.quiet, timeout=self.timeout))
        return self._MDSconn()

    # ---------
    def _cached_fetch(self, mds_connection_cache_ID, TDI):
        action, server0, treename0, shot0, var = mds_connection_cache_ID
        ID = (server0, shot0, treename0, var, TDI)
        data = _special1
        building_cache = False

        caching = self.caching and OMFITmdsCache().cachesDir

        if caching:
            try:
                data = __HDD_MDS_cache__[ID]
            except KeyError:
                pass

        if caching and data is not _special1:
            printd('MDS cache hit : %s' % (ID,), topic='MDS')

        else:
            if not caching:
                printd('MDS cache skip: %s' % (ID,), topic='MDS')
            else:
                printd('MDS cache miss: %s' % (ID,), topic='MDS')
            tunneled_server = tunneled_MDSserver(server0, quiet=self.quiet)
            connection_cache_key = (action, tunneled_server, treename0, shot0)

            if connection_cache_key not in list(self.MDSconn.keys()) or not hasattr(self, '_data'):
                # connect to MDS+
                data = self.MDSconn.mdsvalue(tunneled_server, treename0, shot0, TDI, timeout=self.timeout)
                printd('* Connect and retrieve data ' + TDI, topic='MDS')
            else:
                # already connected
                try:
                    data = mdsplus_data(self.MDSconn[connection_cache_key].get(TDI, timeout=self.timeout))
                    if self.treename is None and data is not None and len(data)==1 and data[0]==0:
                        raise Exception('Try local PTDATA')
                    printd('* Retrieving remote data ' + TDI, topic='MDS')
                except Exception as _excp:
                    try:
                        data = mdsplus_data(MDSplus.TdiExecute(TDI))
                        printd('* Retrieving local data ' + TDI, topic='MDS')
                    except Exception:
                        if 'Try local PTDATA' in repr(_excp):
                            pass
                        else:
                            raise _excp

            # return None if there is no data
            if data is _special1:
                data = None
            else:
                data = b2s(data)

            if caching:
                __HDD_MDS_cache__[ID] = data
                building_cache = True

        return copy.copy(data), building_cache

    # DATA (and checks if data is in the node)
    def _fetch_data(self):

        # unique variable identifier on the server side
        if not hasattr(self, 'server0'):
            self.interpret_id()
        var = omfit_hash(str((self.server0, self.treename0, self.shot0, self.TDI)),10)
        mds_connection_cache_ID = ('read', self.server0, self.treename0, self.shot0, var)

        # fetch data
        if not hasattr(self, '_data') or self._data is _special1:
            tmp, building_cache = self._cached_fetch(mds_connection_cache_ID, '_s{}={}'.format(var, self.TDI))

            if tmp is _special1:
                if not self.quiet:
                    printi('No data in node ' + self.TDI)

            elif tmp is not None:
                self._data = np.atleast_1d(tmp)

                if building_cache:
                    # HDD cache must be complete for each OMFITmdsValue
                    self._fetch_units()
                    self._fetch_dim_of()
                    self._fetch_units_dim_of()
                    self._fetch_error()
                    self._fetch_error_dim_of()

        return mds_connection_cache_ID, var

    # DIM_OF
    def _fetch_dim_of(self):
        mds_connection_cache_ID, var = self._fetch_data()
        if not hasattr(self, '_data') or self._data is _special1:
            return

        if not hasattr(self, '_dim_of'):
            self._dim_of = {}
            for k in range(len(self._data.shape)):
                self._dim_of[k] = None
                try:
                    self._dim_of[k], building_cache = self._cached_fetch(mds_connection_cache_ID, 'dim_of(_s' + var + ',' + str(k) + ')')
                    if self._dim_of[k] is not None:
                        self._dim_of[k] = np.atleast_1d(self._dim_of[k])
                except Exception:
                    pass

    # UNITS
    def _fetch_units(self):
        mds_connection_cache_ID, var = self._fetch_data()
        if not hasattr(self, '_data') or self._data is _special1:
            return

        if not hasattr(self, '_units'):
            self._units = None
            try:
                self._units, building_cache = self._cached_fetch(mds_connection_cache_ID, 'units(_s' + var + ')')
            except Exception:
                pass

    # UNITS_DIM_OF
    def _fetch_units_dim_of(self):
        mds_connection_cache_ID, var = self._fetch_data()
        if not hasattr(self, '_data') or self._data is _special1:
            return

        if not hasattr(self, '_units_dim_of'):
            self._units_dim_of = {}
            for k in range(len(self._data.shape)):
                try:
                    self._units_dim_of[k], building_cache = self._cached_fetch(mds_connection_cache_ID, 'units(dim_of(_s' + var + ',' + str(k) + '))')
                except Exception:
                    pass

    # ERROR
    def _fetch_error(self):
        mds_connection_cache_ID, var = self._fetch_data()
        if not hasattr(self, '_data') or self._data is _special1:
            return

        if not hasattr(self, '_error'):
            self._error = None
            try:
                self._error, building_cache = self._cached_fetch(mds_connection_cache_ID, 'error_of(_s' + var + ')')
                if self._error is not None:
                    self._error = np.atleast_1d(self._error)
            except Exception:
                pass

    # ERROR_DIM_OF
    def _fetch_error_dim_of(self):
        mds_connection_cache_ID, var = self._fetch_data()
        self._fetch_error()
        if not hasattr(self, '_data') or self._data is _special1:
            return

        if not hasattr(self, '_error_dim_of'):
            self._error_dim_of = {}
            if self._error is not None:
                for k in range(len(self._error.shape)):
                    self._error_dim_of[k] = None
                    try:
                        self._error_dim_of[k], building_cache = self._cached_fetch(mds_connection_cache_ID, 'error_of(dim_of(_s' + var + ',' + str(k) + '))')
                        if self._error_dim_of[k] is not None:
                            self._error_dim_of[k] = np.atleast_1d(self._error_dim_of[k])
                    except Exception:
                        pass

    # ---------
    def write(self, xarray_data):
        '''
        write data to node

        :param xarray_data: multidimensional data to be written to MDS+ node in the format of an xarray.DataArray

        :return: outcome of MDSplus.put command
        '''

        # handle ssh connection and expressions
        if not hasattr(self, 'server0'):
            self.interpret_id()
        tunneled_server = tunneled_MDSserver(self.server0, quiet=self.quiet)

        # write to MDS+ node
        return self.MDSconn.write(tunneled_server, self.treename0, self.shot0, self.TDI, xarray_data)

    # ---------
    def __str__(self):
        return str(self.data())

    def __repr__(self):
        return self.__class__.__name__ + '(' + ','.join(map(repr, [self.server, self.treename, self.shot, self.TDI])) + ')'

    def fetch(self):
        """
        Connect to MDS+ server and fetch ALL data: data, units, dim_of, units_dim_of, error, error_dim_of

        :return: None
        """
        self._fetch_data()

        self._fetch_units()

        self._fetch_dim_of()

        self._fetch_units_dim_of()

        self._fetch_error()

        self._fetch_error_dim_of()

    def __call__(self):
        """
        Connect to MDS+ server and fetch the data

        :return: None
        """
        return self._base_data()

    def _slice(self, data, cut_value=None, cut_dim=0, interp='nearest', bounds_error=True):
        if cut_dim > len(np.atleast_1d(self._data).shape) - 1:
            raise MDSplus.MdsInvalidEvent('cut_dim > than number of data dimensions')

        if len(data.shape) == 1:
            return interpolate.interp1d(self.dim_of(0), data, kind=interp, bounds_error=bounds_error)(cut_value)

        if len(data.shape) == 2:
            if cut_dim == 0:
                return interpolate.interp1d(self.dim_of(0), data, kind=interp, bounds_error=bounds_error)(cut_value)
            if cut_dim == 1:
                return interpolate.interp1d(self.dim_of(1), data.T, kind=interp, bounds_error=bounds_error)(cut_value)

    def data(self, cut_value=None, cut_dim=0, interp='nearest', bounds_error=True):
        '''
        :param cut_value: value of dimension `cut_dim` along which to perform the cut

        :param cut_dim: dimension along which to perform the cut

        :param interp: interpolation of the cut: nearest, linear, cubic

        :param bounds_error: whether an error is raised if `cut_value` exceeds the range of `dim_of(cut_dim)`

        :return: If `cut_value` is None then return the MDS data.
                 If `cut_value` is not None, then return data value at `cut_value` for dimension `cut_dim`
        '''
        data = self._base_data()

        if cut_value is None or data is None:
            return data
        else:
            return self._slice(data, cut_value=cut_value, cut_dim=cut_dim, interp=interp, bounds_error=bounds_error)

    def error(self, cut_value=None, cut_dim=0, interp='nearest', bounds_error=True):
        '''
        :param cut_value: value of dimension `cut_dim` along which to perform the cut

        :param cut_dim: dimension along which to perform the cut

        :param interp: interpolation of the cut: nearest, linear, cubic

        :param bounds_error: whether an error is raised if `cut_value` exceeds the range of `dim_of(cut_dim)`

        :return: If `cut_value` is None then return the MDS error.
                 If `cut_value` is not None, then return error value at `cut_value` for dimension `cut_dim`
        '''
        error = self._base_error()

        if cut_value is None or error is None:
            return error
        else:
            return self._slice(error, cut_value=cut_value, cut_dim=cut_dim, interp=interp, bounds_error=bounds_error)

    @property
    def help(self):
        return self.idConnStr() + " : " + str(self.TDI)

    def __tree_repr__(self):
        if not hasattr(self, '_data') or self._data is _special1:
            values = [self.help, []]
        else:
            values = [self.data(), ['MDSactive']]
        return values

    def __save_kw__(self):
        return {'server': self.server, 'shot': self.shot, 'treename': self.treename, 'TDI': self.TDI, 'quiet': self.quiet, 'caching': self.caching}

    def check(self, check_dim_of=0, debug=False):
        """
        Checks whether a valid result has been obtained or not (could be missing data, bad pointname, etc.)

        :param check_dim_of: int
            if check_dim_of >= 0: check that .dim_of(check_dim_of) is valid
            else: disable additional check

        :param debug: bool
            Return a dictionary containing all the flags and relevant information instead of a single bool

        :return: bool or dict
            False if a data problem is detected, otherwise True.
            If `debug` is true: dict containing debugging information relating to the final flag
        """
        try:
            data = self._base_data()
        except Exception:  # It is appropriate for this exception to be broad since it is checking if the thing worked.
            if debug:
                return dict(data_failed_early=True)
            return False

        # If treename is None, the MDS wrapper can check DIII-D's PTDATA system. A failed call here returns data = [0].
        if self.treename is None:
            bad_ptdata = len(np.atleast_1d(data)) == 1 and np.atleast_1d(data)[0] == 0
        else:
            bad_ptdata = False

        # If treename is not None, data are looked for in MDS and a failure returns data = None.
        # Also check [None], just in case.
        bad_mdsdata = data is None or (len(np.atleast_1d(data)) == 1 and np.atleast_1d(data)[0] is None)

        if check_dim_of >= 0:
            try:
                cdim = self.dim_of(check_dim_of)
            except Exception:
                if debug:
                    return dict(data_failed_early=False, dim_failed=True)
                return False
            # If treename is None, the MDS wrapper can check DIII-D's PTDATA system. Failed call here returns data=[0].
            if self.treename is None:
                bad_ptdim = len(np.atleast_1d(cdim)) == 1 and np.atleast_1d(data)[0] == 0
            else:
                bad_ptdim = False

            # If treename is not None, data are looked for in MDS and a failure returns data = None.
            bad_mdsdim = cdim is None or (len(np.atleast_1d(cdim)) == 1 and np.atleast_1d(cdim)[0] is None)
        else:
            bad_mdsdim = False
            bad_ptdim = False
            cdim = None

        if debug:
            return dict(
                result=not (bad_mdsdata or bad_ptdata or bad_mdsdim or bad_ptdim),
                bad_mdsdata=bad_mdsdata,
                bad_ptdata=bad_ptdata,
                bad_mdsdim=bad_mdsdim,
                bad_ptdim=bad_ptdim,
                check_dim_of=check_dim_of,
                data_failed_early=False,
                dim_failed=False,
                data=data,
                cdim=cdim,
            )
        else:
            return not (bad_mdsdata or bad_ptdata or bad_mdsdim or bad_ptdim)

    def plot(self, *args, **kw):
        '''
        plot method based on xarray

        :return: current axes
        '''
        tmp = self.xarray()
        tmp.plot(*args, **kw)
        coords = list(tmp.coords.keys())
        if len(tmp.coords) == 1 and 'units' in tmp[coords[0]].attrs:
            pyplot.gca().set_xlabel(tmp[coords[0]].attrs['units'])
        elif len(tmp.coords) == 2:
            if 'units' in tmp[coords[0]].attrs:
                pyplot.gca().set_xlabel(tmp[coords[0]].attrs['units'])
            if 'units' in tmp[coords[1]].attrs:
                pyplot.gca().set_ylabel(tmp[coords[1]].attrs['units'])
        return pyplot.gca()

    # End of class OMFITmdsValue


# ==================
# Signal interpreter
# ==================

known_units = {}


def get_dss_thom_units(shot, ch=None, pointname=None, latex_form=False):
    """
    Defines units for signals DS*THOM*
    These are not listed in PTDATA but it is easy to figure them out and they shouldn't be left blank
    :param shot: int
    :param ch: int
        Supply channel number, as the logical channels in detachment control can be Te or ne.
    :param pointname: string
        Used to determine channel number, if ch is None
    :param latex_form: bool
        Format string with LaTeX (better for use in plots)
    :return: string
    """
    if ch is None:
        ch = int((re.findall(r'\d+', pointname))[0])
    assert 1 <= ch <= 4, 'PCS detachment control uses logical TS channels 1-4, so ch {} is invalid'.format(ch)
    m = OMFITmdsValue(server='DIII-D', shot=shot, treename=None, TDI='DSITHOM{}Q'.format(ch))
    return 'eV' if np.median(m.data()) == 1 else '10$^{19}$m$^{-3}$' if latex_form else '1e19 m^-3'


def get_dss_radp_units(shot, pointname=None, latex_form=False):
    """
    Defines units for DS*RADP* signals
    These are not listed in PTDATA but they can be determined fairly easily; they should not be left blank
    :param shot: int
    :param pointname: string
    :param latex_form: bool (unused, but provided for consistency)
    :return: string
    """
    printd('keyword latex_form to get_dss_radp_units with value {} is ignored'.format(latex_form))
    if re.search(r'DS[ST]RADP[G]*[1-4].*', pointname, re.IGNORECASE):
        m = OMFITmdsValue(server='DIII-D', shot=shot, treename=None, TDI='DSIRADP_CONVERT')
        convert = m.data().max() if m.check() else 0
        if re.search(r'DS[ST]RADPG[1-4].*', pointname, re.IGNORECASE):
            # The groups are MW or AU, depending on conversion
            # Technically, unconverted units are W, but they lose their meaning in the sum, so use AU to avoid confusion
            return 'MW' if convert else 'AU'
        elif re.search(r'DSSTRADP\+', pointname, re.IGNORECASE):
            # Individual channels are W or MW
            return 'MW' if convert else 'AU'
    elif pointname.upper().startswith('PCBOLO'):
        return 'V'
    else:
        printe('Unrecognized radp pointname {}'.format(pointname))
        return ''


def get_gas_command_units(shot=None, pointname=None, latex_form=False):
    """
    Determines units of a gas command
    Not returned by PTDATA calls, but not exactly unknown, either.
    :param shot: int
    :param pointname: string
    :param latex_form: bool
    :return: string
    """
    printd(
        'keywords shot, pointname, and latex_form to get_gas_command_units with '
        'values {}, {}, {} are ignored'.format(shot, pointname, latex_form)
    )

    return 'V'


def interpret_signal(server=None, shot=None, treename=None, tdi=None, scratch=None):
    """
    Interprets a signal like abc * def by making multiple MDSplus calls.

    MDSplus might be able to interpret expressions like abc*def by itself,
    but sometimes this doesn't work (such as when the data are really in PTDATA?)

    You might also have already cached or want to cache abc and def locally
    because you need them for other purposes.

    :param server: string
        The name of the MDSplus server to connect to

    :param shot: int
        Shot number to query

    :param treename: string or None
        Name of the MDSplus tree. None is for connecting to PTDATA at DIII-D.

    :param tdi: string
        A pointname or expression containing pointnames
        Use 'testytest' as a fake pointname to avoid connecting to MDSplus during testing

    :param scratch: dict-like [optional]
        Catch intermediate quantities for debugging by providing a dict

    :return: (array, array, string/None, string/None)
        x: independent variable
        y: dependent variable as a function of x
        units: units of y or None if not found
        xunits: units of x or None if not found
    """

    def printq(*args):
        """printd with consistent topic assignment"""
        return printd(*args, topic='interpret_signal')

    printq('interpreting signal server {server:}, shot {shot:}, treename {treename:}, tdi {tdi:}'.format(**locals()))
    if tdi is None:
        printq('done interpreting signal (early exit)')
        return None, None, None, None
    tdis = re.split(r'[\*\+\-\/]', tdi)
    printq('    tdis {}'.format(tdis))

    # Set defaults
    x = None
    ys = []
    units = []
    xu = None
    bad_xu = bad = [[], '', None, 'none', 'None']

    # Loop through individual signals in the product and gather each
    for i, td in enumerate(tdis):
        try:
            _ = float(td)
        except ValueError:
            can_be_number = False
        else:
            can_be_number = True
        if td is None or server is None or shot is None or can_be_number:
            ys += [None]
            units += ['']
            printq('  skip fetching & interp for {} (i = {}, can_be_number = {})'.format(td, i, can_be_number))
            continue
        m = OMFITmdsValue(server=server, treename=treename, shot=shot, TDI=td.strip())
        if not m.check():
            printw('Warning: bad MDS data for {}#{}, tree {}, {}'.format(server, shot, treename, td))
            return None, None, '', ''
        x1 = m.dim_of(0).astype(float)
        y1 = m.data().astype(float)
        u1 = b2s(m.units())
        xu1 = m.units_dim_of(0)
        if scratch is not None:
            scratch['mds{}'.format(i)] = m
            scratch['tdi{}'.format(i)] = td
            scratch['x{}'.format(i)] = x1
            scratch['y{}'.format(i)] = y1
        printq('    signal interpreter found units {} and xunits {} for {}'.format(repr(u1), repr(xu1), td))
        # Resolve x units
        if (xu in bad_xu) and (xu1 not in bad_xu):
            printq('    signal interpreter updating xunits from {} to {}'.format(repr(xu), repr(xu1)))
            xu = xu1
        else:
            if xu != xu1:
                # OH NO
                if xu1 in bad:
                    printw('Signal {} has bad X units ({}) that do not match other signals.'.format(td, repr(xu1)))
                elif xu not in bad:
                    printe(
                        'ERROR! X units of {} do not match established x units for {}! This case is probably junk! '
                        'Analysis will proceed to facilitate debugging.'.format(td, tdi)
                    )
                else:
                    printq('    old and potential new xunits are both bad: {} and {}'.format(repr(xu), repr(xu1)))
        # Resolve x data. This is simple: the first non-None data become THE x data.
        if x is None:
            x = x1
        # Resolve y data. Copy the 1st entry. Subsequent entries may have to be interpolated.
        if not len(ys):
            ys += [y1]
        else:
            if np.array_equal(x, x1):
                ys += [y1]
            else:
                ys += [interp1d(x1, y1, bounds_error=False, fill_value=np.NaN)(x)]
        # Resolve y units. We have to assemble a string with all the units we caught.
        if not u1.strip():
            # Handle units for recognized signals that don't have units stored in MDSplus/PTDATA
            u1 = known_units.get(td, '')
            printq('        signal interpreter updated {} units to {} using known_units dictionary'.format(td, u1))
            if not u1.strip() and re.search(r'DS[STI]THOM[1-4].*', td):
                u1 = get_dss_thom_units(shot, pointname=td)
                printq('        signal interpreter updated {} units to {} using get_dss_thom_units()'.format(td, u1))
            elif not u1.strip() and re.search(r'[GD]AC.*', td):
                u1 = get_gas_command_units(shot, pointname=td)
                printq('        signal interpreter updated {} units to {} using get_gas_command_units()'.format(td, u1))

        units += [u1]
        printq('    after {}, units are now {} and xunits are {}'.format(td, repr(units), repr(xu)))
        # Done with this entry. New data should be multiplied into y.

    # Should now have a list of y arrays and a list of units. Time to combine them.
    instruction = copy.copy(tdi)
    final_units = copy.copy(tdi)
    for i, td in enumerate(tdis):
        printq(
            '  updating instruction / final units for i = {}, td = {}, instruction = {}, final_units = {}'.format(
                i, td, instruction, final_units
            )
        )
        if ys[i] is not None:
            instruction = instruction.replace(td, 'ys[{}]'.format(i))
            final_units = final_units.replace(td, units[i])
        else:
            final_units = final_units.replace(td, '')

    printq('instruction to be evaluated: {}'.format(instruction))
    y = eval(instruction)

    if isinstance(scratch, dict):
        scratch['x'] = x
        scratch['raw_units'] = copy.copy(final_units)

    # Cleanup units
    final_units = final_units.strip()
    ops = '*/+-'
    # Remove any leading/trailing operators
    while np.any([final_units.startswith(a) or final_units.endswith(a) for a in ops]):
        for a in ops:
            printq('   signal interpreter units cleanup on {}...'.format(repr(final_units)))
            if final_units.startswith(a):
                final_units = final_units[1:].strip()
            if final_units.endswith(a):
                final_units = final_units[:-1].strip()
    printq('   signal interpreter units cleanup finished: {}'.format(repr(final_units)))

    printq(
        'Done interpreting signal. Shape(y)={}, x range: {},{} {}'.format(np.shape(y), np.nanmin(x), np.nanmax(x), xu)
    )
    return x, y, final_units if final_units is None else final_units.strip(), xu if xu is None else xu.strip()


# ======================
# backward compatibility
# ======================
mdsValue = OMFITmdsValue


def solveMDSserver(server):
    server = translate_MDSserver(server, '')
    server = SERVER[server]['MDS_server']
    server = parse_server(server)[2]
    return server


############################################
if '__main__' == __name__:
    test_classes_main_header()
    # Turn cache on and off
    OMFITmdsCache(False)
    OMFITmdsCache(True)
    # Initialize a class instance without connecting; should be very fast
    mdsstring = '.cer.cerauto.vertical.channel33:time'
    OMFITmdsValue(server='D3D', treename='IONS', shot=171646, TDI=mdsstring)
