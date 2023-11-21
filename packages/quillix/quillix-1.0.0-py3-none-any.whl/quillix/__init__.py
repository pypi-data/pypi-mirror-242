import json
import os
import pandas as pd
import re

class conditionNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

data = {"default": {}}
database = "default"

def loadData():
    if os.path.exists('data.json'):
        with open("data.json", "r") as f:
            data.update(json.load(f))

def saveData():
    global env
    with open("data.json", "w") as f:
        json.dump(data, f)
        env = True

def createDB(name):
    loadData()

    flag = True

    for dbName in data:
        if dbName == name:
            print('Database already exists...')
            flag = False
            break

    if flag:
        data.update({name: {}})
        saveData()
        useDB(name)

def useDB(name):
    loadData()
    flag = False

    for db in data:
        if db == name:
            flag = True
            global database
            database = name
            break

    if flag == False:
        print("Database does not exist...")

def createTable(name, columns):
    loadData()
    flag = True

    for table in data[database]:
        if table == name:
            print('Table already exists...')
            flag = False
            break

    if flag:
        if len(columns) == len(set(columns)):
            data[database].update({name: {"architecture": columns, "records": []}})
            saveData()
        else:
            print("Duplicate column names are not allowed...")

def insertData(tableName, columnName, recordData):
    loadData()

    colCheck = True
    dbCheck = False
    tableCheck = False

    for db in data:
        if db == database:
            dbCheck = True
            for table in data[db]:
                if table == tableName:
                    tableCheck = True
                    for column in columnName:
                        if column not in data[db][table]["architecture"]:
                            colCheck = False
                            print('"'+column+'" does not exist in "'+table+'"...')
                            break
    
    if dbCheck:
        if tableCheck:
            if colCheck:
                mapData = []
                for column in data[database][tableName]["architecture"]:
                    if column in columnName:
                        mapData.append(recordData[columnName.index(column)])
                    else:
                        mapData.append(None)

                data[database][tableName]["records"].append(mapData)
                saveData()
        else:
            print('Invalid table name...')
    else:
        print('Invalid Database name...')

def drop(dtype, obj):
    loadData()

    if dtype == "table":
        for tableName in data[database]:
            if tableName == obj:
                del data[database][obj]
                break
    elif dtype == "database":
        if obj == database:
            print("Database in use...")
        else:
            for db in data:
                if db == obj:
                    del data[obj]
                    break
    else:
        print("There is no "+dtype+" by the name '"+obj+"'")

    saveData()

def truncate(table):
    loadData()

    for tableName in data[database]:
        if tableName == table:
            data[database][table]["records"] = []
            break

    saveData()

def showDB():
    loadData()

    for db in data:
        print(db)

def showTables():
    loadData()
    count = 0

    for table in data[database]:
        count = count + 1
        print(table)

    if count == 0:
        print("Database is empty...")

def genTree(expression):
    if not expression:
        return None

    if expression[1] in {'AND', 'OR', 'and', 'or'}:
        root = conditionNode(expression[1])

        root.left = genTree(expression[0])
        root.right = genTree(expression[2])
    else:
        root = conditionNode(expression)

    return root

def alterLeafNodes(root, data):

    def traverse(node):
        if node is not None and len(node.value) > 1:
            if node.left is None and node.right is None and len(node.value) == 3:
                column_name, operator, value = node.value
                if value not in data.columns:
                    condition = data[column_name].apply(lambda x: eval(f'x {operator} value', globals(), {'value': value, 'x': x}))
                else:
                    condition = data.apply(lambda row, col=column_name, val=value: eval(f'row["{col}"] {operator} row["{val}"]', globals(), {'val': val, 'row': row}), axis=1)
                
                node.value = condition[condition].index.tolist()
            else:
                traverse(node.left)
                traverse(node.right)

    traverse(root)
    return root

def evalTree(binaryData):

    if binaryData.left is not None and binaryData.right is not None:
        if isinstance(binaryData, list):
            return binaryData

        left_result = evalTree(binaryData.left)
        right_result = evalTree(binaryData.right)

        if binaryData.value.lower() == "or":
            return list(set(left_result) | set(right_result))
        elif binaryData.value.lower() == "and":
            return list(set(left_result) & set(right_result))
    else:    
        return binaryData.value
    
def showData(tableName, conditions):
    loadData()

    dbCheck = False
    tableCheck = False

    for db in data:
        if db == database:
            dbCheck = True
            for table in data[db]:
                if table == tableName:
                    tableCheck = True

    if dbCheck:
        if tableCheck:
            record_Data = pd.DataFrame(data[database][tableName]["records"], columns = data[database][tableName]["architecture"])
            if len(conditions) > 0:
                record_Data = record_Data.loc[evalTree(alterLeafNodes(genTree(conditions), record_Data))]

            return record_Data

def updateData(tableName, col, op, val, conditions):
    loadData()

    colCheck = True
    dbCheck = False
    tableCheck = False

    for db in data:
        if db == database:
            dbCheck = True
            for table in data[db]:
                if table == tableName:
                    tableCheck = True
                    for column in col:
                        if column not in data[db][table]["architecture"]:
                            colCheck = False
                            print('"'+column+'" does not exist in "'+table+'"...')
                            break

    if dbCheck:
        if tableCheck:
            if colCheck:
                record_Data = pd.DataFrame(data[database][tableName]["records"], columns = data[database][tableName]["architecture"])
                record_Data.fillna('null', inplace=True)
                if len(conditions) > 0:
                    indices = evalTree(alterLeafNodes(genTree(conditions), record_Data))
                else:
                    indices = [i for i in range(len(record_Data))]
                
                for index, record in record_Data.iterrows():
                    if index in indices:
                        for element in zip(col, op, val):
                            if element[1] == "=":
                                record_Data.at[index, element[0]] = element[2]
                            elif element[1] == "+":
                                record_Data.at[index, element[0]] = record_Data.at[index, element[0]] + element[2]
                            elif element[1] == "-":
                                record_Data.at[index, element[0]] = record_Data.at[index, element[0]] - element[2]
                            elif element[1] == "*":
                                record_Data.at[index, element[0]] = record_Data.at[index, element[0]] * element[2]
                            elif element[1] == "/":
                                record_Data.at[index, element[0]] = record_Data.at[index, element[0]] / element[2]
                            else:
                                record_Data.at[index, element[0]] = record_Data.at[index, element[0]] % element[2]

                dlist = record_Data.values.tolist()
                dlist = [[None if val == 'null' else val for val in record] for record in dlist]
                data[database][tableName]["records"] = dlist
                saveData()
        else:
            print('Invalid table name...')
    else:
        print('Invalid Database name...')

def deleteData(tableName, conditions):
    loadData()

    dbCheck = False
    tableCheck = False

    for db in data:
        if db == database:
            dbCheck = True
            for table in data[db]:
                if table == tableName:
                    tableCheck = True

    if dbCheck:
        if tableCheck:
                record_Data = pd.DataFrame(data[database][tableName]["records"], columns = data[database][tableName]["architecture"])
                record_Data.fillna('null', inplace=True)

                record_Data.drop(evalTree(alterLeafNodes(genTree(conditions), record_Data)), inplace=True)

                dlist = record_Data.values.tolist()
                dlist = [[None if val == 'null' else val for val in record] for record in dlist]
                data[database][tableName]["records"] = dlist
                saveData()
        else:
            print('Invalid table name...')
    else:
        print('Invalid Database name...')

def alterTable(tableName, type, alterValues):
    loadData()

    dbCheck = False
    tableCheck = False

    for db in data:
        if db == database:
            dbCheck = True
            for table in data[db]:
                if table == tableName:
                    tableCheck = True

    if dbCheck:
        if tableCheck:
                if type.lower() == "add":
                    data[database][tableName]["architecture"].append(alterValues[0])
                    for record in data[database][tableName]["records"]:
                        record.append(None)
                elif type.lower() == "rename":
                    for i in range(len(data[database][tableName]["architecture"])):
                        if data[database][tableName]["architecture"][i] == alterValues[0]:
                            data[database][tableName]["architecture"][i] = alterValues[1]
                elif type.lower() == "drop":
                    index = data[database][tableName]["architecture"].index(alterValues[0])
                    data[database][tableName]["architecture"].pop(index)

                    for record in data[database][tableName]["records"]:
                        record.pop(index)        
                else:
                    print('Invalid keyword "'+type+'"...')

                saveData()
        else:
            print('Invalid table name...')
    else:
        print('Invalid Database name...')

def tokenize(expression):
    tokens = re.findall(r'\(|\)|\w+|==|>=|<=|!=|>|<|AND|OR', expression)
    return tokens

def parse(tokens):
    current = []
    while tokens:
        token = tokens.pop(0)
        if token == '(':
            current.append(parse(tokens))
        elif token == ')':
            break
        elif token.isdigit():
            current.append(int(token))
        else:
            current.append(token)
    return current

def convert_to_array(expression):
    tokens = tokenize(expression)
    parsed_array = parse(tokens)
    return parsed_array

def replace_columns(query, table_info):
    for alias, _, suffix in table_info:
        query = re.sub(fr'(?<!\w){alias}\.(\w+)', fr'\g<1>{suffix}', query, flags=re.IGNORECASE)
    return query

def query(query):
    parts = query.strip().split(" ")

    if parts[0].lower() == "use":
        useDB(parts[1])
    elif parts[0].lower() == "create": 
        if parts[1].lower() == "table":
            createTable(parts[2], re.search(r'\((.*?)\)', query).group(1).replace(' ', '').split(','))
        elif parts[1].lower() == "database":
            createDB(parts[2])
        else:
            print('Invalid syntax...')
    elif parts[0].lower() == "insert" and parts[1].lower() == "into":
        opening_bracket_indices = [index for index, char in enumerate(query) if char == '(']
        closing_bracket_indices = [index for index, char in enumerate(query) if char == ')']
        elements = query[opening_bracket_indices[1] + 1 : closing_bracket_indices[1]].replace(' ', '').split(',')
        elements = [float(element) if element.strip().replace('.', '').isdigit() else element for element in elements]
        insertData(parts[2], query[opening_bracket_indices[0] + 1 : closing_bracket_indices[0]].replace(' ', '').split(','), elements)
    elif parts[0].lower() == "drop":
        drop(parts[1], parts[2])
    elif parts[0].lower() == "show":
        if parts[1].lower() == "databases":
            showDB()
        elif parts[1].lower() == "tables":
            showTables()
        else:
            print('Invalid syntax...')
    elif parts[0].lower() == "truncate":
        if parts[1]:
            truncate(parts[1])
        else:
            print('Missing argument...')
    elif parts[0].lower() == "delete" and parts[1].lower() == "from":
        conditions = query[query.lower().index("where") + 5:].strip().replace(' ', '')
        conditions = conditions[1:-1]

        if conditions:
            deleteData(parts[2], convert_to_array(conditions))
        else:
            print('No valid criteria for deletion...')
    elif parts[0].lower() == "alter" and parts[1].lower() == "table":
        alterVal = []
        alterVal.append(parts[5])

        if len(parts) > 6:
            alterVal.append(parts[7])

        alterTable(parts[2], parts[3], alterVal)
    elif parts[0].lower() == "update" and parts[1].lower() == "table":
        columns = []
        operators = []
        values = []

        if query.lower().find("where") != -1:
            conditions = query[query.lower().index("where") + 5:].strip().replace(' ', '')
            conditions = conditions[1:-1]
            clause = query[query.lower().find("set") + 3:query.lower().find("where")]
        else:
            conditions = False
            clause = query[query.lower().find("set") + 3:]

        clause = clause.strip().replace(' ', '').split(',')
        for element in clause:
            match = re.match(r'([a-zA-Z0-9_]+)([+\-*/%=])([a-zA-Z0-9_]+)', element)

            columns.append(match.group(1))
            operators.append(match.group(2))
            values.append(int(match.group(3)) if match.group(3).isdigit() else match.group(3))

        if conditions:
            updateData(parts[2], columns, operators, values, convert_to_array(conditions))
        else:
            updateData(parts[2], columns, operators, values, [])
    elif parts[0].lower() == "select":
        colChecker = True

        if '.' not in query:

            match = re.search(r'\bFROM\b\s+(\w+)', query, re.IGNORECASE)
            if match:
                table_name = match.group(1)
            else:
                print("No table name found after 'FROM'")

            if query.lower().find("where") != -1:
                match = re.search(r'\bWHERE\b\s+(.*?)(?:GROUP BY|ORDER BY|$)', query, re.DOTALL | re.IGNORECASE)

                if match:
                    conditions = match.group(1)
                    conditions = conditions[1:-1]

                    recData = showData(table_name, convert_to_array(conditions))
                else:
                    print("No conditions found inside 'WHERE'")
            else:
                recData = showData(table_name, [])
        else:
            from_clause = re.search(r'FROM (.+?) WHERE', query, re.IGNORECASE).group(1)
            table_info = [item.strip().split() + ['_' + chr(ord('x') + i)] for i, item in enumerate(from_clause.split(','))]
            query = replace_columns(query, table_info)
            
            df1 = showData(table_info[0][1], [])
            df1.columns = [f'{col}_x' for col in df1.columns]

            df2 = showData(table_info[1][1], [])
            df2.columns = [f'{col}_y' for col in df2.columns]

            recData = pd.merge(df1, df2, left_index=True, right_index=True)

            if query.lower().find("where") != -1:
                match = re.search(r'\bWHERE\b\s+(.*?)(?:GROUP BY|ORDER BY|$)', query, re.DOTALL | re.IGNORECASE)

                if match:
                    conditions = match.group(1)
                    conditions = conditions[1:-1]

                    indices = evalTree(alterLeafNodes(genTree(convert_to_array(conditions)), recData))
            
            recData = recData.loc[indices]
            
        if "group by" in query.lower():
            colChecker = False
            if "order by" in query.lower():
                groupByColumns = query[query.lower().find("group by") + 8:query.lower().find("order")]
            else:
                groupByColumns = query[query.lower().find("group by") + 8:]

            group = groupByColumns.replace(' ', '').split(',')

            if query.lower().find("count") != -1:
                Str = query[query.lower().find("count") + 5:].split()[0]
                countCol = Str[1:-1].replace(' ', '')
                recData = recData.groupby(group).size().reset_index(name=countCol)
            elif query.lower().find("avg") != -1:
                Str = query[query.lower().find("avg") + 3:].split()[0]
                avgCol = Str[1:-1].replace(' ', '').split(',')
                recData = recData.groupby(group).agg({col: 'mean' for col in avgCol}).reset_index()
            elif query.lower().find("sum") != -1:
                Str = query[query.lower().find("sum") + 3:].split()[0]
                sumCol = Str[1:-1].replace(' ', '').split(',')
                recData = recData.groupby(group).agg({col: 'sum' for col in sumCol}).reset_index()
        else:
            if query.lower().find("count") != -1:
                colChecker = False
                Str = query[query.lower().find("count") + 5:].split()[0]
                countCol = Str[1:-1].replace(' ', '').split(',')
                count_results = pd.DataFrame(columns=['Column', 'Count'])

                for col in countCol:
                    count_results = pd.concat([count_results, pd.DataFrame({'Column': [col], 'Count': [recData[col].count()]})], ignore_index=True)
                
                recData = count_results
            
            elif query.lower().find("avg") != -1:
                colChecker = False
                Str = query[query.lower().find("avg") + 3:].split()[0]
                avgCol = Str[1:-1].replace(' ', '').split(',')
                count_results = pd.DataFrame(columns=['Column', 'Average'])

                for col in avgCol:
                    count_results = pd.concat([count_results, pd.DataFrame({'Column': [col], 'Average': [recData[col].mean()]})], ignore_index=True)
                
                recData = count_results
            elif query.lower().find("sum") != -1:
                colChecker = False
                Str = query[query.lower().find("sum") + 3:].split()[0]
                sumCol = Str[1:-1].replace(' ', '').split(',')
                count_results = pd.DataFrame(columns=['Column', 'Sum'])

                for col in sumCol:
                    count_results = pd.concat([count_results, pd.DataFrame({'Column': [col], 'Sum': [recData[col].sum()]})], ignore_index=True)
                
                recData = count_results

        if "order by" in query.lower():
            if "asc" in query.lower():
                order = query[query.lower().find("order by") + 8:query.lower().find("asc")].replace(' ', '').split(',')
                oType = True
            elif "desc" in query.lower():
                order = query[query.lower().find("order by") + 8:query.lower().find("desc")].replace(' ', '').split(',')
                oType = False
            else:
                order = query[query.lower().find("order by") + 8:].replace(' ', '').split(',')
                oType = True
            
            recData = recData.sort_values(by=order, ascending=[oType])

        if colChecker:
            clDt = query[query.lower().find("select") + 6:query.lower().find("from")].replace(' ', '').split(',')
            if clDt[0] != '*':
                recData = recData[clDt]

        return recData