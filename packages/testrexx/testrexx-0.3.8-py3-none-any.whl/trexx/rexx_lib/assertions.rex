

Assert_True:                                                           
    expression_string = Arg(1)                                         
    Interpret 'expression_value ='expression_string                    
    If expression_value == 1 Then                                      
     Call Increment_Test_Stem 'SUCCESS,'||expression_string||' is True'
    Else                                                               
     Call Increment_Test_Stem 'FAIL,'||expression_string||' is False'  
    Return
                                                                       
Increment_Test_Stem:                                                   
    trexx_iterator = trexx_iterator + 1                                
    trexx_tests.trexx_iterator = Arg(1)                                
    Return                                                             
                                                                       
Display_Test_Result:                                                   
    Do i = 1 to trexx_iterator                                         
      Say '%TEST'||i||'='trexx_tests.i                                  
    End                                                                
    Return                                                             