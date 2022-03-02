import io

with io.StringIO("hello") as f:
    print(f.read())
