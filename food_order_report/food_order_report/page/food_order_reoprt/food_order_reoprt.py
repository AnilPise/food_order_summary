import requests
import frappe

# food_order_report.food_order_report.page.food_order_reoprt.food_order_reoprt.fetch_food_orders
@frappe.whitelist()
def fetch_food_orders(month=1):
	try:
		url = "http://canteen.benzyinfotech.com/api/v3/customer/report"
		headers = {
		    'Content-Type': "application/json",
		    'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiZWRhNWExODU0OTFhYWE0MmY5YzMyZjRhMTU5MDM1ODk4ZjZiMzMxNWUzZjJjNGRiZDA1N2IyNGE3NTAzMDc3NDBlMjFlYjZmNGE4Mjk0MGUiLCJpYXQiOjE3MDQ4MDA4OTAuODc5OTI1OTY2MjYyODE3MzgyODEyNSwibmJmIjoxNzA0ODAwODkwLjg3OTkyOTA2NTcwNDM0NTcwMzEyNSwiZXhwIjoxNzM2NDIzMjkwLjgzNDkxMjA2MTY5MTI4NDE3OTY4NzUsInN1YiI6IjI2NSIsInNjb3BlcyI6W119.CwDEjlHoRtOXdFcaO6KGGxV202AOA7MMtJVPtKzgLqzTFzUUnDLGBd7PNAtHO2--3YOathM9HOG8hYjY8wjktXZIoCGUR9GWIaEVUxLwFq927CrSf05NuqTBTrJcDeBOjXDvKcSBiJ2A994FC2IunPcdkaZ4jpoaWBIaWueYUbHviYSQuLec3tFcAMg4njrImAlaN9k-QKkHetpdrdbUEX1Wzq4X-1QwuOx7W3W2nbbxaoNgFX1gaabxi00ZO7h5MokGvtqy_gCkS9TYoM74VfxmTyAAczjttLcPqDNiAL_ZJdutDMezw32CZj8G8l8PUL46F_BuaxatZDBUZxeClZh4_0Wvo9GX4zqF2XvHdzZHnwdB414vNCl8itaGW9w7QWbdchPOglhnek32ZmkH0MIqeOBhnAyHo5_WbP0uLd_3qmz3w04nvTbTGV25-QebaxPAsVD0-7Za1sVpqB_FD6yEeliaEzdxl_8gA5IH59uowpfPYgUIjom8NVEASuYsAwb0q3f0jhNRfwg2zmXNenoDunh_dN9l2NRjI2gdZueSMwu6IJLQK46jpn01uG2iQ1xx-pFJAGe_bzSceLsho3dbtabym3tMqi0Ac02xUP9Mn50LdkFJGNVU9jiuHQfyjQirDtGUfya3aIvpJlCGx9Cx99s_4P89uDnOiXy3A1Q"
		}
		data = {
		    "month": int(month)
		}

		response = requests.post(url, headers=headers, json=data)

		if response.status_code != 200:
			frappe.throw("Failed to fetch data from API")

		data = response.json()
		user_data = data.get("user")
		order_data = data.get("reports")

		final_data = {
			"id": user_data.get("id"),
			"f_name": user_data.get("f_name"),
			"l_name": user_data.get("l_name"),
			"phone": user_data.get("phone"),
			"email": user_data.get("email"),
			"emp_id": user_data.get("emp_id")
		}

		report_data = []
		total_fine = 0
		for i in order_data:

			if isinstance(i.get("opt_ins"), dict):
				opts = i.get("opt_ins")
				fine = 0
				for ord_status in opts.values():
					if ord_status == "Pending":
						fine += 100
				total_fine += fine


				summ = [
					{
						'name': "breakfast",
						'status': opts.get("breakfast"),
						'fine': 100 if opts.get("breakfast") == "Pending"  else ""
					},
					{
						'name': "lunch",
						'status':opts.get("lunch"),
						'fine':100 if opts.get("lunch") == "Pending"  else ""
					},
					{
						'name': "dinner",
						'status':opts.get("dinner"),
						'fine':100 if opts.get("dinner") == "Pending"  else ""
					}
				]
			else:
				summ = [
					{
						'name': "breakfast",
						'status': "-",
						'fine':""
					},
					{
						'name': "lunch",
						'status':"-",
						'fine':""
					},
					{
						'name': "dinner",
						'status':"-",
						'fine':""
					}
				]


			temp_dict = {
				'date': i.get("date"),
				'food_options': summ
			}
			report_data.append(temp_dict)

		final_data["total_fine"] = total_fine
		final_data["order_details"] = report_data
		return final_data
		
	except Exception as e:
		raise e