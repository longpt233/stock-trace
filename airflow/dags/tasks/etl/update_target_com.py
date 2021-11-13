from monggodb import getAllCompany


# load name_price_v1 loc cac thu roi day len v2 
def updateV2():
    all = getAllCompany()

    target1 =[]

    for dict in all: 
        if dict.get("price") <30000 : 
            target1.append(dict)


    print(target1)
