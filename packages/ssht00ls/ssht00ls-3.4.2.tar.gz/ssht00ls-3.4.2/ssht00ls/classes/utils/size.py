import os, sys, fil3s
size = None
path = sys.argv[1]
if not os.path.exists(path):
	r3sponse.log(response=r3sponse.error(f"Path {path} does not exist."))
else:
	r3sponse.log(response=r3sponse.success(f"Successfully retrieved the size of {path}.", {
		"size":Formats.FilePath(path).size(mode="MB"),
	}))