CREATE PROCEDURE PROCEDURE `insert_phrase`(
in L_ID int,
in All_Titles Text,
in All_Headers Text,
in All_Others Text
)
BEGIN
DECLARE word Text;
DECLARE _nextlen1 int;
DECLARE _value1 Text;
Declare i int;
set i = 0;
iterator:
LOOP  
  IF LENGTH(TRIM(All_Titles)) = 0 OR All_Titles IS NULL THEN
    LEAVE iterator;
  END IF;
  set i = i + 1;

  SET word = SUBSTRING_INDEX(All_Titles,',',1);
  SET _nextlen1 = LENGTH(word);
  SET _value1 = TRIM(word);
  
  INSERT INTO phrase(word,L_ID,Pos,W_Type)
  values(word,L_ID,i,"Title");
    
  SET All_Titles = INSERT(All_Titles,1,_nextlen1 + 1,'');
END LOOP;

set i = 0;
iterator:
LOOP  
  IF LENGTH(TRIM(All_Headers)) = 0 OR All_Headers IS NULL THEN
    LEAVE iterator;
  END IF;
  set i = i + 1;

  SET word = SUBSTRING_INDEX(All_Headers,',',1);
  SET _nextlen1 = LENGTH(word);
  SET _value1 = TRIM(word);
  
  INSERT INTO phrase(word,L_ID,Pos,W_Type)
  values(word,L_ID,i,"Header");
    
  SET All_Headers = INSERT(All_Headers,1,_nextlen1 + 1,'');
END LOOP;
set i = 0;
iterator:
LOOP  
  IF LENGTH(TRIM(All_Others)) = 0 OR All_Others IS NULL THEN
    LEAVE iterator;
  END IF;
  set i = i + 1;

  SET word = SUBSTRING_INDEX(All_Others,',',1);
  SET _nextlen1 = LENGTH(word);
  SET _value1 = TRIM(word);
  
  INSERT INTO phrase(word,L_ID,Pos,W_Type)
  values(word,L_ID,i,"Other");
    
  SET All_Others = INSERT(All_Others,1,_nextlen1 + 1,'');
END LOOP;
END