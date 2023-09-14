MODULE EGMPositionStream
    
    !***********************************************************    
    !
    ! Module: NDI_EGM
    !
    ! Description:
    !   Returns position data for robot as it executes a predetermined path.
    !
    ! Author: Jonas Beachy, Boeing Advanced Research Center, University of Washington
    ! Version: 1.0
    !
    !***********************************************************
    
    ! Starting "Home" Position and path target points
    CONST jointtarget ready:=[[-90,0,0,0,90,0], [9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1:=[[100,-250,400],[0,0.707106781,0.707106781,0],[-1,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];    
    CONST robtarget Target_2:=[[-100,-250,400],[0,0.707106781,0.707106781,0],[-1,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_3:=[[-100,-450,400],[0,0.707106781,0.707106781,0],[-1,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];   
    CONST robtarget Target_40:=[[100,-450,400],[0,0.707106781,0.707106781,0],[-1,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_50:=[[100,-250,400],[0,0.707106781,0.707106781,0],[-1,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];    
    
    ! Tool Data
    TASK PERS tooldata Dummy:=[TRUE,[[0,0,0],[1,0,0,0]],[1,[0,0,1],[1,0,0,0],0,0,0]];
  
    ! Work Object Data 
    TASK PERS wobjdata Example:=[FALSE,TRUE,"",[[0,0,0],[1,0,0,0]],[[0,0,0],[1,0,0,0]]];
    
    
    VAR egmident egmID1;
    VAR egmstate egmSt1;
    ! limits for cartesian convergence: +-1 mm
    CONST egm_minmax egm_minmax_lin1:=[-1,1];
    ! limits for orientation convergence: +-2 degrees
    CONST egm_minmax egm_minmax_rot1:=[-2,2];

    !***********************************************************
    !
    ! Procedure main
    !
    !***********************************************************
   
    PROC main()
        
!        Rob_Motion;
        EGM_Proc;
        
    ENDPROC
    
    PROC EGM_Proc()

        EGMReset egmID1;
        EGMGetId egmID1;
        egmSt:=EGMGetState(egmID1);
        TPWrite "EGM state: "\Num:=egmSt;
        
        IF egmSt1<=EGM_STATE_CONNECTED THEN
            !Configuration-Communication-Transmission Protocol: 
            !       Set IP address and Port for computer/sensor as well as device name
            !       In this case the device name is UCdevice, IP=127.0.0.1, Port=6510
            EGMSetupUC ROB_1,egmID1,"default","UCdevice:"\Pose \CommTimeout:=10000;
        ENDIF
        
        !Stream position ever 4 ms
        EGMStreamStart egmID1\SampleRate:=4;
        Rob_Motion;
        EGMStreamStop egmID1;
        egmSt:=EGMGetState(egmID1);
        
        IF egmSt=EGM_STATE_CONNECTED THEN
            TPWrite "Reset EGM instance egmID";
            EGMReset egmID1;  
        ENDIF
    
    ENDPROC
    
    PROC Rob_Motion()
        MoveAbsJ ready, v200, z5, Dummy\WObj:=Example;
        WaitTime 2;
        MoveJ Target_1,v200,z5,Dummy\WObj:=Example;
        WaitTime 2;
        MoveL Target_2,v50,z5,Dummy\WObj:=Example;
        WaitTime 2;
        MoveL Target_3,v50,z5,Dummy\WObj:=Example;
        WaitTime 2;
        MoveL Target_40,v50,z5,Dummy\WObj:=Example;
        WaitTime 2;
        MoveL Target_50,v50,z5,Dummy\WObj:=Example;
        WaitTime 2;
        MoveAbsJ ready, v200, z5, Dummy\WObj:=Example;
        EGMReset egmID1; 
    ENDPROC
    
ENDMODULE