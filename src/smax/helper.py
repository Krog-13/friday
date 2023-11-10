async def prepare_post_params(data, person):
    """
    """
    category = "\n".join(data["subcategory"])
    _message = f"Категория обращения:\n{category}\nОписание проблемы: {data['problem']}" \
              f"\nНомер кабинета: {data['cabinet']}\nНомер телефона: {data['phone']}" \
              f"\n\nАвтор обращения: {person[5]}" \
              f"\nРуководитель: {person[6]}" \
              f"\nТелефон: {person[3]}" \
              f"\nПочта: {person[2]}"
    query_param = {"entities": [
        {
            "entity_type": "Request",
            "properties": {
                # "RequestedForPerson": "163490",
                "RequestedByPerson": "163490",
                "Active": True,
                "PhaseId": "Log",
                "DisplayLabel": "Тестовый запрос Smart-bot",
                "Description": _message,
                "ImpactScope": "SingleUser",
                "Urgency": "SlightDisruption",
                "RequestType": "ServiceRequest",
                "CurrentAssignment": "Unassigned",
                "CreationSource": "CreationSourceOther",
                # "RequestsOffering": "153226"
            }
        }
    ],
        "operation": "CREATE"
    }
    return query_param


async def get_id_order(response):
    # get id from response
    order_id = response["entity_result_list"][0]["entity"]["properties"]["Id"]
    return order_id
