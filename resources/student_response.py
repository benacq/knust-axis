from dateutil import parser


class StudentResponse:

    @staticmethod
    def shape_response(student):
        student_response = {}

        if "notes" in student["_attrs"] and student["_attrs"]["notes"] == "student":
            student_response["first_names"] = student["_attrs"]["firstName"]
            student_response["last_name"] = student["_attrs"]["lastName"]
            student_response["full_name"] = student["_attrs"]["fullName"]
            student_response["reference_number"] = student["_attrs"]["pager"]
            student_response["enrollment_date"] = student["_attrs"]["createTimeStamp"]
            student_response["student_email"] = student["_attrs"].get("email", "N/A")

            student_response["department"] = student["_attrs"].get("department") if "department" in student["_attrs"] \
                else student["_attrs"].get("workState", "N/A")

            student_response["college"] = student["_attrs"].get("company") if "company" in student["_attrs"] \
                else student["_attrs"].get("workCountry", "N/A")

        new_enrollment_date = parser.parse(str(student_response["enrollment_date"]))
        student_response["enrollment_date"] = new_enrollment_date

        return student_response
