


import logging

try:
    import qtgui
except Exception as e:
    logging.error(e, exc_info=True)
    raise Exception("Error in App") #to raise errors in app during coding

