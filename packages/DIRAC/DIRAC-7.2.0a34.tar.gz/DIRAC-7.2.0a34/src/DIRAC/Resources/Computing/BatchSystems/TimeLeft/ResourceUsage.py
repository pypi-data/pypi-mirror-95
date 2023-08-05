"""
Resource Usage
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os

from DIRAC import gLogger


class ResourceUsage(object):
  """ Resource Usage is an abstract class that has to be implemented for every batch system used by DIRAC
      to get the resource usage of a given job. This information can then be processed by other modules
      (e.g. getting the time left in a Pilot)
  """

  def __init__(self, batchSystemName, jobIdEnvVar):
    """ Standard constructor
    """
    self.log = gLogger.getSubLogger('%sResourceUsage' % batchSystemName)
    self.jobID = os.environ.get(jobIdEnvVar)

  def getResourceUsage(self):
    """ Returns a dictionary containing CPUConsumed, CPULimit, WallClockConsumed
        and WallClockLimit for current slot.  All values returned in seconds.

        :return: dict such as {cpuConsumed, cpuLimit, wallClockConsumed, wallClockLimit}
    """
    raise NotImplementedError("getResourceUsage not implemented")
