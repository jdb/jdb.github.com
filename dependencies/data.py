
# deps is a model for a set of dependencies: for each keys, there is
# the list of dependencies: key requires list of dependencies

deps = {
  "log"     : ["snmp","json"],
  "psi"     : ["common"],
  "a"       : ["log"],
  "media"   : ["a", "psi", "common"],
  "avc"     : ["a", "common"],
  "ts"      : ["a", "psi", "avc", "media"],
  "rtp"     : ["a", "psi", "common", "media"],
  "mp4"     : ["common", "a", "media"],
  "vod"     : ["a", "media", "rtp", "mp4", "avc", "log", "ts"]}

deps = {
  1   : [2,3],
  5   : [4],
  6   : [1],
  7   : [6, 5, 4],
  8   : [6, 4],
  9   : [6, 5, 8, 7],
  11  : [6, 5, 4, 7],
  10  : [4, 6, 7],
  12  : [6, 7, 11, 10, 8, 1, 9]}


