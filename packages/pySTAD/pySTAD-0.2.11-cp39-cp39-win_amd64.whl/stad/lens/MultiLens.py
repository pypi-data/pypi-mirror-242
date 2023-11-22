import numpy as np
from stad import lens

class MultiLens:
  """
  A helper class to apply multiple lenses in STAD. 

  Construct a MultiLens with Lens objects. 

  After running STAD, this class contains a mask indicating the edges between 
  non-adjacent bins of the lens and a list of the fitted Lens objects.

  Parameters
  ----------
  lenses: 
    The Lens objects to use.

  Attributes
  ----------
  lenses : 
    A list with the individual Lens objects
  non_adjacent_edges :
    A mask indicating which edges connect nodes in non-adjacent filter segments.
  """
  def __init__(self, *lenses):
    """
    Constructs a MultiLens object

    Parameters
    ---------
    lenses : 
      The Lens objects to combine.
    """
    self.lenses = lenses
  
  def __call__(self, sparse_distances):
    """
    Used internally to find the non-adjacent edges, which are suppressed in the
    output.
    """
    mask = np.ones(sparse_distances.data.shape, dtype = bool)
    for lens in self.lenses:
      mask = mask & lens(sparse_distances)
    self.non_adjacent_edges = ~mask
    return mask