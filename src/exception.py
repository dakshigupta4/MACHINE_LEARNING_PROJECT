import sys
def error_message_detail(error,error_detail:sys):
    _,_,exc_tab=error_detail.exc_info()
    file_name=exc_tab.tb_frame.f_code.co_filename
    error_message="Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(file_name,exc_tab.tb_lineno,str(error))
    return error_message
class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message,error_detail=error_detail)
    def __str__(self):
        return self.error_message
# if __name__=="__main__":
#     try:
#         a=1/0
#     except Exception as e:
#         obj=CustomException(e,sys)
#         print(obj)
# This code makes error messages more readable and detailed, instead of just saying "Error: division by zero", it tells you exactly where and why the error occurred.