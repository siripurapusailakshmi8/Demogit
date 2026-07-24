temp_dict = [{"name" : "sai", "company": "microsoft"}, [{"name": "satish", "company": "vetafore"}, {"name": "tarun", "company": "bms"}], ("revanth","epam")]

for record in temp_dict:
    if (isinstance(record, dict)):
        print(f'{record["name"]} is working in {record["company"]}')
    elif (isinstance(record, list)):
        for sub_record in record:
            print(f'{sub_record["name"]} is working in {sub_record["company"]}')
    elif(isinstance(record, tuple)):
        print(f'{record[0]} is working in {record[1]}')
        print("hello world , this is for git demo")
        print("hey ")
