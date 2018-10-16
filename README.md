# PyZabbix_excel_report
this is a scrit which could help you to extract zabbix problems statistics and export to excel

file pyzabbix_excell_report2.py can receive arguments:
                                                      <b>-g</b> [or --group] -> argument extract problem from specific hostgroup {ex: -g Switches}
                                                      if you have a group branch like Work/Office1/Switches ,Work/Office1/Workstation
                                                      you can receive all problems to specific 'hostgroup branch' with usaje of *[asterics/multiplication]
                                                      in this case uning argument -g Work/Office1/* will receive all problem from groups Work/Office1/Switches
                                                      and Work/Office1/Workstation
                                                      
                                                      <b>-v</b> -> extract problems in status 'PROBLEM' or 'RESOLVED'
                                                      -v 1 [value=1] will extract problems with status 'PROBLEM'
                                                      -v 0 [value=0] will extract problems with status 'RESOLVED'
                                                      without this argument will extract both
                                                      
                                                      <b>--time_from</b> -> (seconds) with how long ago will receive problems [actual time- time_from parameter(seconds)]
                                                      by default without this argument will receive 2 hours ago problems { you can change in script [row 92]}
                                                      
                                                      <b>--time_till</b> -> (seconds) until receive the problems [actual time- time_from parameter(seconds)]
                                                      
                                                      
