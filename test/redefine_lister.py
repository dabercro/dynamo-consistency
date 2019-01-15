from dynamo_consistency import remotelister
from dynamo_consistency.backend import test
from dynamo_consistency.backend import listers

# Do the listing through the listers.Lister interface
# so that the IgnoreDirectories list of the old version is used
class TestLister(listers.Lister):
    def __init__(self):
        super(TestLister, self).__init__(0, 'TEST')

    def ls_directory(self, path):
        return test._ls(path)

remotelister.get_listers = lambda _: (TestLister, [(), ()])
