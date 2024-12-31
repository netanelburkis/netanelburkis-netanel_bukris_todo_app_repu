from flask import Flask, render_template, request
from datetime import datetime

todo_list_app = Flask(__name__)

tasks = []

@todo_list_app.route('/', methods=['GET', 'POST'])
@todo_list_app.route('/<user_input>', methods=['GET', 'POST'])
def main_page_todo_list__app(user_input=""):
    user = user_input
    
    if request.method == 'POST':
        action = request.form.get('action')
        task = request.form.get('task')
        task_id = request.form.get('task_id')
        
        if action == 'add' and task:
            task_data = {
                'task': task,
                'completed': False,  
                'date_added': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'task_id': len(tasks) + 1  
            }
            tasks.append(task_data)
        elif action == 'del' and task:
            tasks[:] = [t for t in tasks if t['task'] != (task)]   
        elif action == 'del' and task_id:
            tasks[:] = [t for t in tasks if t['task_id'] != int(task_id)]
        elif action == 'toggle' and task_id:
            
            for t in tasks:
                if t['task_id'] == int(task_id):
                    t['completed'] = not t['completed']
    
    query = request.form.get('search', '')
    filtered_tasks = [task for task in tasks if query.lower() in task['task'].lower()]
    
    return render_template('main_page_todo_list.html', user=user, tasks=filtered_tasks, query=query)

@todo_list_app.route('/by_netanel_bukris')
def by_netanel_bukris():
    return render_template('by_netanel_bukris.html')

if __name__ == "__main__":
    todo_list_app.run(debug=True)