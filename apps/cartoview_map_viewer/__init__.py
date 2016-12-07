import os
APP_NAME = os.path.basename(os.path.dirname(__file__))
urls_dict = {
    'admin': {'%s.new' % APP_NAME: 'Create new'},
}