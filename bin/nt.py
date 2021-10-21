
# Copyright 2021 ThinkPool, all rights reserved
"""
"""

__appname__ = 'content-manager'
__version__ = '1.0'


import optparse
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import naver_keyword_search as nks
from naver_keyword_search.keyword_manager import KeywordManager

if __name__ == '__main__':
    usage = """%prog [options]"""
    parser = optparse.OptionParser(usage=usage, description=__doc__)
    parser.add_option("--content", metavar="CONTENT", dest="content",
                      help="content name")
    nks.add_basic_options(parser)
    (options, args) = parser.parse_args()

    config_dict = nks.read_config_file(options.config_file)
    config_dict['app_name'] = __appname__
    log_dict = config_dict.get('log', {})
    log_file_name = f"{options.content}.log"
    nks.setup_logging(appname=__name__, appvers=__version__,
                      filename=log_file_name, dirname=options.log_dir,
                      debug=options.debug, log_dict=log_dict,
                      emit_platform_info=True)
    # if options.content == 'naver':        
    KeywordManager().run(config_dict)
    # else:
    #     print('Content 이름 확인')        
