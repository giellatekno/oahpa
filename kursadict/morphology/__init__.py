""" Morphology module.
"""

from morphology import ( Tagsets
                       , Tag
                       , XFST
                       , OBT
                       , Morphology
                       , pregeneration_tag_rewrites
                       )

# Import to register the functions
import morphological_definitions

__all__ = [ 'XFST'
          , 'OBT'
          , 'Morphology'
          , 'morphological_definitions'
          , 'pregeneration_tag_rewrites'
          ]

