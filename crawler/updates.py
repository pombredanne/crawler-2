from crawler.detectors import *
from crawler.manifest import subst_vars

class UpdateFinder(object):

	def find_update(self, manifest):
		update = {}

		# Copy static fields:
		for f in ["name", "license"]:
			try:
				update[f] = manifest[f]
			except KeyError:
				pass

		detectors_cache = {}
		detectors = manifest["detectors"]
		for what in ["version"] + [k for k in detectors.keys() if k != "version"]:
			for detector_type, detector_options in detectors[what].iteritems():
				try:
					detector = detectors_cache[detector_type]
				except KeyError:
					detector = Detector.create(detector_type, manifest)

				detector.detect(what, detector_options, update)
				# Substitute version in all manifest properties:
				if what == "version":
					subst_vars(manifest, {"VERSION": update["version"]})

		return update

