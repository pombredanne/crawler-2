from dependencywatcher.crawler.detectors import Detector
from dependencywatcher.crawler.utils import VersionUtil
import urllib2, json, logging

logger = logging.getLogger(__name__)

class JSDelivrDetector(Detector):
    """ jsdelivr.com API based information detector """
    url = "http://api.jsdelivr.com/v1/jsdelivr/libraries/%s"

    def __init__(self, manifest):
        self.json = None
        super(JSDelivrDetector, self).__init__(manifest) 

    def get(self, library_name):
        url = JSDelivrDetector.url % library_name
        logger.debug("Opening URL: %s" % url)
        r = json.load(urllib2.urlopen(url))
        return r[0] if len(r) > 0 else None

    def detect(self, what, options, result):
        if self.json is None:
            library_name = self.manifest["name"]
            self.json = self.get(library_name)
            if not self.json and not "-" in library_name and not library_name.endswith("js"):
                self.json = self.get(library_name + "js")
            if not self.json and "-" in library_name:
                self.json = self.get(library_name.replace("-", "."))
        try:
            if what == "url":
                result[what] = self.normalize(what, self.json["homepage"])
            elif what == "description":
                result[what] = self.normalize(what, self.json["description"])
            elif what == "version":
                result[what] = self.normalize(what, self.json["lastversion"])
            elif what == "updatetime":
                result[what] = self.parse_date(self.json["meta"]["created"])
            elif what == "stable_version":
                result[what] = VersionUtil.find_stable(self.json["versions"])
        except KeyError:
            pass

