from flask import request, jsonify
from flask_restful import Resource
from modelos import db, User, Project, PersonalProjects
from hashlib import *



class Orchestrator(Resource):
   
    def post(self):
        try:
           
            token = request.headers.get('Authorization')
            #username = request.args.get('username')
            user_name = 'abc'

            #if token and username:
            if user_name and token:

                data = request.json
                request_user = User.query.filter(User.username == user_name).first()
                if not request_user:
                    return {"message": "Usuario no encontrado"}, 404
                else:
                    new_project = Project(
                        company_id = request_user.id,
                        project_name = data["project"]["project_name"],
                        description = data["project"]["description"],
                        creation_date = data["project"]["creation_date"],
                        end_date = data["project"]["end_date"]
                    )
                    db.session.add(new_project)
                    db.session.commit()

                    if new_project.id:
                        project_info_data = data.get("personal_projects")
                        if project_info_data:
                            for project_info in project_info_data:
                                new_project_info = PersonalProjects(
                                    company_id = request_user.id,
                                    project_id = new_project.id,
                                    fullName = project_info["fullName"],
                                    project_role = project_info["project_role"]
                                )
                                db.session.add(new_project_info)
                    
                        db.session.commit()
                        return {"message": "Proyecto creado correctamente", "id": new_project.id}, 201            
            else:
                return jsonify({"message": "Falta el token en el encabezado de la solicitud"}), 401

        except KeyError as e:
            return {'message': f'Key error: {str(e)}'}, 400
    


class Ping(Resource):
    def get(self):
        return "pong", 200
    

class Health(Resource):
    def get(self):
        return "pong", 200    




   
