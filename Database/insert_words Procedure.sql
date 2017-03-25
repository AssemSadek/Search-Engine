CREATE PROCEDURE PROCEDURE `insert_words`(
in All_Words Text,
in L_ID int,
in TF nvarchar(4000),
in No_Titles nvarchar(4000),
in No_Headers nvarchar(4000),
in No_Others nvarchar(4000)
)
BEGIN
DECLARE word1 Text;
DECLARE TF1 nvarchar(4000);
DECLARE No_Titles1 nvarchar(4000);
DECLARE No_Headers1 nvarchar(4000);
DECLARE No_Others1 nvarchar(4000);
DECLARE _nextlen1 int;
DECLARE _value1 nvarchar(4000);
DECLARE _nextlen3 int;
DECLARE _value3 nvarchar(4000);
DECLARE _nextlen4 int;
DECLARE _value4 nvarchar(4000);
DECLARE _nextlen5 int;
DECLARE _value5 nvarchar(4000);
DECLARE _nextlen6 int;
DECLARE _value6 nvarchar(4000);

iterator:
LOOP
  IF LENGTH(TRIM(All_Words)) = 0 OR All_Words IS NULL THEN
    LEAVE iterator;
  END IF;

  SET word1 = SUBSTRING_INDEX(All_Words,',',1);
  SET _nextlen1 = LENGTH(word1);
  SET _value1 = TRIM(word1);
  
  SET TF1 = SUBSTRING_INDEX(TF,',',1);
  SET _nextlen3 = LENGTH(TF1);
  SET _value3 = TRIM(TF1);
  
  SET No_Titles1 = SUBSTRING_INDEX(No_Titles,',',1);
  SET _nextlen4 = LENGTH(No_Titles1);
  SET _value4 = TRIM(No_Titles1);
  
  SET No_Headers1 = SUBSTRING_INDEX(No_Headers,',',1);
  SET _nextlen5 = LENGTH(No_Headers1);
  SET _value5 = TRIM(No_Headers1);
  
  SET No_Others1 = SUBSTRING_INDEX(No_Others,',',1);
  SET _nextlen6 = LENGTH(No_Others1);
  SET _value6 = TRIM(No_Others1);

  
  INSERT INTO words(word,L_ID,TF,No_Titles,No_Headers,No_others) 
  values(word1,L_ID,CAST(TF1 AS UNSIGNED),CAST(No_Titles1 AS UNSIGNED),CAST(No_Headers1 AS UNSIGNED),CAST(No_others1 AS UNSIGNED));
    
  SET All_Words = INSERT(All_Words,1,_nextlen1 + 1,'');
  SET TF = INSERT(TF,1,_nextlen3 + 1,'');
  SET No_Titles = INSERT(No_Titles,1,_nextlen4 + 1,'');
  SET No_Headers = INSERT(No_Headers,1,_nextlen5 + 1,'');
  SET No_Others = INSERT(No_Others,1,_nextlen6 + 1,'');
  
  
  
END LOOP;
END