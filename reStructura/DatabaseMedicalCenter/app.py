import os
import logging
import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from db_config import get_db_connection
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, SignupForm, BusinessModelForm, ComponentForm
from models import User, BusinessModel, CustomerSegment, CustomerRelationship, ValueProposition, Channel, RevenueStream, KeyResource, KeyActivity, KeyPartnership, CostStructure

#Test CI
# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Context processor to add current_year to all templates
@app.context_processor
def inject_current_year():
    return {'current_year': datetime.datetime.now().year}

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, name, email, role FROM Users WHERE user_id=%s", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return User(id=user[0], name=user[1], email=user[2], role=user[3])
    return None

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = generate_password_hash(form.password.data)
        role = form.role.data

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Users (name, email, password, role) VALUES (%s, %s, %s, %s)", 
                          (name, email, password, role))
            conn.commit()
            flash('Signup successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            conn.rollback()
            app.logger.error(f"Error signing up: {e}")
            flash(f'Error signing up: Email may already be registered', 'danger')
        finally:
            conn.close()
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, name, email, password, role FROM Users WHERE email=%s", (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[3], password):
            user_obj = User(id=user[0], name=user[1], email=user[2], role=user[4])
            login_user(user_obj)
            
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                if user[4] == 'admin':
                    next_page = url_for('admin_dashboard')
                else:
                    next_page = url_for('dashboard')
            
            return redirect(next_page)
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    
    # Get user's business models or models shared with the user if they are an investor
    if current_user.role == 'investor':
        cursor.execute("""
            SELECT bm.model_id, bm.business_name, bm.industry, bm.created_at, u.name as owner_name 
            FROM BusinessModels bm
            JOIN Users u ON bm.user_id = u.user_id
            ORDER BY bm.created_at DESC
        """)
    else:
        cursor.execute("""
            SELECT model_id, business_name, industry, created_at 
            FROM BusinessModels 
            WHERE user_id=%s 
            ORDER BY created_at DESC
        """, (current_user.id,))
    
    models = cursor.fetchall()
    conn.close()
    
    return render_template('dashboard.html', models=models)

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied: Admin privileges required', 'danger')
        return redirect(url_for('dashboard'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get all users
    cursor.execute("SELECT user_id, name, email, role FROM Users")
    users = cursor.fetchall()
    
    # Get all business models
    cursor.execute("""
        SELECT bm.model_id, bm.business_name, u.name, bm.created_at 
        FROM BusinessModels bm
        JOIN Users u ON bm.user_id = u.user_id
        ORDER BY bm.created_at DESC
    """)
    models = cursor.fetchall()
    
    conn.close()
    
    return render_template('admin_dashboard.html', users=users, models=models)

@app.route('/create_model', methods=['GET', 'POST'])
@login_required
def create_model():
    if current_user.role == 'investor':
        flash('Investors cannot create business models', 'warning')
        return redirect(url_for('dashboard'))
        
    form = BusinessModelForm()
    if form.validate_on_submit():
        business_name = form.business_name.data
        industry = form.industry.data
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO BusinessModels (user_id, business_name, industry) VALUES (%s, %s, %s) RETURNING model_id",
                (current_user.id, business_name, industry)
            )
            model_id = cursor.fetchone()[0]
            conn.commit()
            flash('Business Model created successfully!', 'success')
            return redirect(url_for('edit_model', model_id=model_id))
        except Exception as e:
            conn.rollback()
            app.logger.error(f"Error creating business model: {e}")
            flash(f'Error creating business model: {e}', 'danger')
        finally:
            conn.close()
            
    return render_template('create_model.html', form=form)

@app.route('/edit_model/<int:model_id>', methods=['GET', 'POST'])
@login_required
def edit_model(model_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if model exists and user has permission
    cursor.execute("SELECT * FROM BusinessModels WHERE model_id=%s", (model_id,))
    model = cursor.fetchone()
    
    if not model:
        conn.close()
        flash('Business model not found', 'danger')
        return redirect(url_for('dashboard'))
        
    # Check if current user is owner or admin
    if current_user.role != 'admin' and model[1] != current_user.id:
        conn.close()
        flash('You do not have permission to edit this business model', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get all components for this model
    components = {}
    
    # Customer Segments
    cursor.execute("SELECT * FROM CustomerSegments WHERE model_id=%s", (model_id,))
    components['customer_segments'] = cursor.fetchall()
    
    # Value Propositions
    cursor.execute("SELECT * FROM ValuePropositions WHERE model_id=%s", (model_id,))
    components['value_propositions'] = cursor.fetchall()
    
    # Channels
    cursor.execute("SELECT * FROM Channels WHERE model_id=%s", (model_id,))
    components['channels'] = cursor.fetchall()
    
    # Customer Relationships
    cursor.execute("SELECT * FROM CustomerRelationships WHERE model_id=%s", (model_id,))
    components['customer_relationships'] = cursor.fetchall()
    
    # Revenue Streams
    cursor.execute("SELECT * FROM RevenueStreams WHERE model_id=%s", (model_id,))
    components['revenue_streams'] = cursor.fetchall()
    
    # Key Resources
    cursor.execute("SELECT * FROM KeyResources WHERE model_id=%s", (model_id,))
    components['key_resources'] = cursor.fetchall()
    
    # Key Activities
    cursor.execute("SELECT * FROM KeyActivities WHERE model_id=%s", (model_id,))
    components['key_activities'] = cursor.fetchall()
    
    # Key Partnerships
    cursor.execute("SELECT * FROM KeyPartnerships WHERE model_id=%s", (model_id,))
    components['key_partnerships'] = cursor.fetchall()
    
    # Cost Structure
    cursor.execute("SELECT * FROM CostStructure WHERE model_id=%s", (model_id,))
    components['cost_structure'] = cursor.fetchall()
    
    conn.close()
    
    return render_template('edit_model.html', model=model, components=components, model_id=model_id)

@app.route('/view_model/<int:model_id>')
@login_required
def view_model(model_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if model exists
    cursor.execute("""
        SELECT bm.*, u.name as owner_name 
        FROM BusinessModels bm
        JOIN Users u ON bm.user_id = u.user_id
        WHERE bm.model_id=%s
    """, (model_id,))
    model = cursor.fetchone()
    
    if not model:
        conn.close()
        flash('Business model not found', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get all components for this model
    components = {}
    
    # Customer Segments
    cursor.execute("SELECT * FROM CustomerSegments WHERE model_id=%s", (model_id,))
    components['customer_segments'] = cursor.fetchall()
    
    # Value Propositions
    cursor.execute("SELECT * FROM ValuePropositions WHERE model_id=%s", (model_id,))
    components['value_propositions'] = cursor.fetchall()
    
    # Channels
    cursor.execute("SELECT * FROM Channels WHERE model_id=%s", (model_id,))
    components['channels'] = cursor.fetchall()
    
    # Customer Relationships
    cursor.execute("SELECT * FROM CustomerRelationships WHERE model_id=%s", (model_id,))
    components['customer_relationships'] = cursor.fetchall()
    
    # Revenue Streams
    cursor.execute("SELECT * FROM RevenueStreams WHERE model_id=%s", (model_id,))
    components['revenue_streams'] = cursor.fetchall()
    
    # Key Resources
    cursor.execute("SELECT * FROM KeyResources WHERE model_id=%s", (model_id,))
    components['key_resources'] = cursor.fetchall()
    
    # Key Activities
    cursor.execute("SELECT * FROM KeyActivities WHERE model_id=%s", (model_id,))
    components['key_activities'] = cursor.fetchall()
    
    # Key Partnerships
    cursor.execute("SELECT * FROM KeyPartnerships WHERE model_id=%s", (model_id,))
    components['key_partnerships'] = cursor.fetchall()
    
    # Cost Structure
    cursor.execute("SELECT * FROM CostStructure WHERE model_id=%s", (model_id,))
    components['cost_structure'] = cursor.fetchall()
    
    conn.close()
    
    return render_template('view_model.html', model=model, components=components)

@app.route('/add_component/<int:model_id>/<string:component_type>', methods=['GET', 'POST'])
@login_required
def add_component(model_id, component_type):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if model exists and user has permission
    cursor.execute("SELECT * FROM BusinessModels WHERE model_id=%s", (model_id,))
    model = cursor.fetchone()
    
    if not model:
        conn.close()
        flash('Business model not found', 'danger')
        return redirect(url_for('dashboard'))
        
    # Check if current user is owner or admin
    if current_user.role != 'admin' and model[1] != current_user.id:
        conn.close()
        flash('You do not have permission to edit this business model', 'danger')
        return redirect(url_for('dashboard'))
    
    form = ComponentForm()
    
    if form.validate_on_submit():
        try:
            if component_type == 'customer_segment':
                cursor.execute(
                    "INSERT INTO CustomerSegments (model_id, segment_name, description) VALUES (%s, %s, %s)",
                    (model_id, form.name.data, form.description.data)
                )
                
            elif component_type == 'customer_relationship':
                cursor.execute(
                    "INSERT INTO CustomerRelationships (model_id, relationship_name, description) VALUES (%s, %s, %s)",
                    (model_id, form.name.data, form.description.data)
                )
                
            elif component_type == 'value_proposition':
                cursor.execute(
                    "INSERT INTO ValuePropositions (model_id, vp_name, description) VALUES (%s, %s, %s)",
                    (model_id, form.name.data, form.description.data)
                )
                
            elif component_type == 'channel':
                cursor.execute(
                    "INSERT INTO Channels (model_id, channel_name, description) VALUES (%s, %s, %s)",
                    (model_id, form.name.data, form.description.data)
                )
                
            elif component_type == 'revenue_stream':
                cursor.execute(
                    "INSERT INTO RevenueStreams (model_id, revenue_name, amount) VALUES (%s, %s, %s)",
                    (model_id, form.name.data, form.amount.data if hasattr(form, 'amount') else 0)
                )
                
            elif component_type == 'key_resource':
                cursor.execute(
                    "INSERT INTO KeyResources (model_id, resource_name, description) VALUES (%s, %s, %s)",
                    (model_id, form.name.data, form.description.data)
                )
                
            elif component_type == 'key_activity':
                cursor.execute(
                    "INSERT INTO KeyActivities (model_id, activity_name, description) VALUES (%s, %s, %s)",
                    (model_id, form.name.data, form.description.data)
                )
                
            elif component_type == 'key_partnership':
                cursor.execute(
                    "INSERT INTO KeyPartnerships (model_id, partner_name) VALUES (%s, %s)",
                    (model_id, form.name.data)
                )
                
            elif component_type == 'cost_structure':
                cursor.execute(
                    "INSERT INTO CostStructure (model_id, cost_name, amount) VALUES (%s, %s, %s)",
                    (model_id, form.name.data, form.amount.data if hasattr(form, 'amount') else 0)
                )
            
            conn.commit()
            flash(f'{component_type.replace("_", " ").title()} added successfully!', 'success')
            return redirect(url_for('edit_model', model_id=model_id))
            
        except Exception as e:
            conn.rollback()
            app.logger.error(f"Error adding component: {e}")
            flash(f'Error adding component: {e}', 'danger')
        finally:
            conn.close()
    
    return render_template('add_component.html', form=form, model_id=model_id, component_type=component_type)

@app.route('/delete_component/<int:model_id>/<string:component_type>/<int:component_id>', methods=['POST'])
@login_required
def delete_component(model_id, component_type, component_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if model exists and user has permission
    cursor.execute("SELECT * FROM BusinessModels WHERE model_id=%s", (model_id,))
    model = cursor.fetchone()
    
    if not model:
        conn.close()
        flash('Business model not found', 'danger')
        return redirect(url_for('dashboard'))
        
    # Check if current user is owner or admin
    if current_user.role != 'admin' and model[1] != current_user.id:
        conn.close()
        flash('You do not have permission to edit this business model', 'danger')
        return redirect(url_for('dashboard'))
    
    try:
        table_map = {
            'customer_segment': 'CustomerSegments',
            'customer_relationship': 'CustomerRelationships',
            'value_proposition': 'ValuePropositions',
            'channel': 'Channels',
            'revenue_stream': 'RevenueStreams',
            'key_resource': 'KeyResources',
            'key_activity': 'KeyActivities',
            'key_partnership': 'KeyPartnerships',
            'cost_structure': 'CostStructure'
        }
        
        id_column_map = {
            'customer_segment': 'segment_id',
            'customer_relationship': 'relationship_id',
            'value_proposition': 'vp_id',
            'channel': 'channel_id',
            'revenue_stream': 'revenue_id',
            'key_resource': 'resource_id',
            'key_activity': 'activity_id',
            'key_partnership': 'partner_id',
            'cost_structure': 'cost_id'
        }
        
        table = table_map.get(component_type)
        id_column = id_column_map.get(component_type)
        
        if not table or not id_column:
            raise ValueError(f"Invalid component type: {component_type}")
            
        cursor.execute(f"DELETE FROM {table} WHERE {id_column}=%s AND model_id=%s", (component_id, model_id))
        conn.commit()
        
        flash(f'{component_type.replace("_", " ").title()} deleted successfully!', 'success')
        
    except Exception as e:
        conn.rollback()
        app.logger.error(f"Error deleting component: {e}")
        flash(f'Error deleting component: {e}', 'danger')
    finally:
        conn.close()
        
    return redirect(url_for('edit_model', model_id=model_id))

@app.route('/delete_model/<int:model_id>', methods=['POST'])
@login_required
def delete_model(model_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if model exists and user has permission
    cursor.execute("SELECT * FROM BusinessModels WHERE model_id=%s", (model_id,))
    model = cursor.fetchone()
    
    if not model:
        conn.close()
        flash('Business model not found', 'danger')
        return redirect(url_for('dashboard'))
        
    # Check if current user is owner or admin
    if current_user.role != 'admin' and model[1] != current_user.id:
        conn.close()
        flash('You do not have permission to delete this business model', 'danger')
        return redirect(url_for('dashboard'))
    
    try:
        cursor.execute("DELETE FROM BusinessModels WHERE model_id=%s", (model_id,))
        conn.commit()
        flash('Business model deleted successfully!', 'success')
    except Exception as e:
        conn.rollback()
        app.logger.error(f"Error deleting model: {e}")
        flash(f'Error deleting model: {e}', 'danger')
    finally:
        conn.close()
        
    return redirect(url_for('dashboard'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error=e, title='Page Not Found'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error=e, title='Server Error'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
