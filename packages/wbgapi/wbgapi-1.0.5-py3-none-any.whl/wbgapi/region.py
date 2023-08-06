
'''Access information about World Bank regions. This works best with the WDI (source=2)
and other databases that share the same list of economies. It will probably not work
well with subnational databases or region-specific ones.
'''
import wbgapi as w
from . import utils
import builtins

def list(id='all', q=None, group=None):
    '''Return a list of regions

    Arguments:
        id:         a region identifier or list-like of identifiers

        q:          search string (on region name)

        group:      subgroup to return. Can be one of: 'admin', 'geo', 'allincomelevels', 'demodividend', 'smallstates', 'other'
                    NB: technically possible to pass 'lending' but the returned values generally aren't useful

    Returns:
        a generator object

    Example:
        regions = {row['code']: row['name'] for row in wbgapi.region.list()}
            
    Notes:
        The region list is global to the entire API and is not specific to the current database.

    '''

    params = {'type': group} if group else {}
    q,_ = utils.qget(q)

    for row in w.fetch('region/' + w.queryParam(id), params):
        if utils.qmatch(q, row['name']):
            yield row

def get(id):
    '''Retrieve the specified region

    Arguments:
        id:         the region ID

    Returns:
        a region object

    Example:
        print(wbgapi.region.get('NAC')['name'])
    '''
    
    
    return w.get('region/' + w.queryParam(id))

def members(id, param='region'):
    '''Return a set of economy identifiers that are members of the specified region

    Arguments:
        id:     a region identifier

        param:  used internally

    Returns:
        a set object of economy identifiers

    Notes:
        the returned members may not match the economies in the current database since we access the universal region lists from the API
    '''

    e = set()
    for row in w.fetch('country', {param: id}):
        e.add(row['id'])

    return e

def Series(id='all', q=None, group=None, name='RegionName'):
    '''Return a pandas Series by calling list
    '''

    return w.Series(list(id, q=q, group=group), key='code', value='name', name=name)

def info(id='all', q=None, group=None):
    '''Print a user report of regions.

    Arguments:
        id:         a region identifier or list-like of identifiers

        q:          search string (on region name)

        group:      subgroup to return. See list() for possible values

    Returns:
        None
            
    Notes:
        The region list is global to the entire API and is not specific to the current database.

    '''

    return w.Featureset(list(id, q=q, group=group), ['code', 'name'])
