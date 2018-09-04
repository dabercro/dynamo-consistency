#! /usr/bin/env python


from dynamo_consistency import picker
from dynamo_consistency import main


if __name__ == '__main__':
    main.main(picker.pick_site())
