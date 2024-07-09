from flask import Flask, request,jsonify, g, session, render_template,send_file
from config import Config
from datetime import timedelta
from app.database.interactions import Interactions
from sqlalchemy import and_, or_
import pandas as pd
import io
app = Flask(__name__)
app.config.from_object(Config)



class Dashbaord:

    """
    Function index
    """
    def index():
        if 'ai_chat_bot_username' not in session:
          return render_template('login.html')

    """
    Function to render the html file
    @param null
    @return render_template
    """
    @staticmethod
    def show():
      if 'ai_chat_bot_username' not in session:
          return render_template('login.html')
      return render_template('dashboard.html')
    
    """
    Function to set the list from databse object
    """
    def interaction_to_dict(interaction):
        return {
            'id': interaction.id,
            'question': interaction.question,
            'response': interaction.response,
            'empid': interaction.empid,
            'raw_question': interaction.raw_question,
            'date': interaction.date,
            'isliked': 'Liked' if interaction.isliked == 1  else 'No Respone' if interaction.isliked is None else 'Disliked',
        }
    
    @staticmethod
    def getData():
       try: 
            if 'ai_chat_bot_username' not in session:
             return render_template('login.html')
            param = request.json
            page = param['page']
            per_page = request.args.get('per_page', 10, type=int)
            employeeDetail = []
            countDetails =[]
            baseUrl = request.host_url
            if page == 1 :
               employeeDetail=  Dashbaord.getEmployeeList()
               countDetails = Dashbaord.getCountDetails()
            interactions = Interactions.query
            
            if param['empid'] is not None and param['empid'] != 'all':
                interactions =interactions.filter_by(empid = param['empid'])

            if param['search'] is not None and param['search'] != '':
                search_term = f"%{param['search']}%"
                interactions =interactions.filter(
                        and_(
                            or_(
                                Interactions.question.ilike(search_term),
                                Interactions.response.ilike(search_term),
                                Interactions.empid.ilike(search_term),
                                Interactions.raw_question.ilike(search_term),
                            )
                        )
                    )

            
            interactions = interactions.paginate(page=page, per_page=per_page, error_out=False)
            

            # Convert the pagination object to a dictionary for JSON response
            interactionsDict = {
                'items': [Dashbaord.interaction_to_dict(interaction) for interaction in interactions.items],
                'total': interactions.total,
                'pages': interactions.pages,
                'current_page': interactions.page,
                'next_num': interactions.next_num,
                'prev_num': interactions.prev_num,
            }
            
            return jsonify({'status': "success", 'base_url' : baseUrl,'data':interactionsDict , 'employee_details':employeeDetail, 'count_details' : countDetails}), 200
       except ValueError as e:
             return jsonify({'status': "failed", 'base_url' : baseUrl , 'message' : e}), 200
       
    def getEmployeeList():
        empDetails = Interactions.query.with_entities(Interactions.empid).group_by(Interactions.empid).all()
        return [item.empid for item in empDetails]
    
    def getCountDetails():

        return {
            'total_count' :  Interactions.query.count(),
            'liked_count' : Interactions.query.filter_by(isliked =True).count(),
            'dislike_count': Interactions.query.filter_by(isliked =False).count(),
            'total_empid': Interactions.query.with_entities(Interactions.empid).group_by(Interactions.empid).count()

        }
    
    def downloadReport():
      
        interactions = Interactions.query.all()
        # Convert the paginated items to a DataFrame
        data = [{
            'id': interaction.id,
            'question': interaction.question,
            'response': interaction.response,
            'empid': interaction.empid,
            'raw_question': interaction.raw_question,
            'date': interaction.date,
            'isliked': 'Liked' if interaction.isliked == 1  else 'No Respone' if interaction.isliked is None else 'Disliked',
        } for interaction in interactions]

        df = pd.DataFrame(data)

        # Convert DataFrame to Excel file in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        output.seek(0)

        return send_file(output, as_attachment=True, download_name=f'report.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
       