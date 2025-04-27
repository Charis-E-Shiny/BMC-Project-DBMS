from flask_login import UserMixin

class User(UserMixin):
    """User model for authentication with Flask-Login"""
    def __init__(self, id, name, email, role):
        self.id = id
        self.name = name
        self.email = email
        self.role = role

class BusinessModel:
    """Business Model class to represent a BMC"""
    def __init__(self, id, user_id, business_name, industry, created_at):
        self.id = id
        self.user_id = user_id
        self.business_name = business_name
        self.industry = industry
        self.created_at = created_at

class CustomerSegment:
    """Customer Segment component of the BMC"""
    def __init__(self, id, model_id, segment_name, description):
        self.id = id
        self.model_id = model_id
        self.segment_name = segment_name
        self.description = description

class CustomerRelationship:
    """Customer Relationship component of the BMC"""
    def __init__(self, id, model_id, relationship_name, description):
        self.id = id
        self.model_id = model_id
        self.relationship_name = relationship_name
        self.description = description

class ValueProposition:
    """Value Proposition component of the BMC"""
    def __init__(self, id, model_id, vp_name, description):
        self.id = id
        self.model_id = model_id
        self.vp_name = vp_name
        self.description = description

class Channel:
    """Channel component of the BMC"""
    def __init__(self, id, model_id, channel_name, description):
        self.id = id
        self.model_id = model_id
        self.channel_name = channel_name
        self.description = description

class RevenueStream:
    """Revenue Stream component of the BMC"""
    def __init__(self, id, model_id, revenue_name, amount):
        self.id = id
        self.model_id = model_id
        self.revenue_name = revenue_name
        self.amount = amount

class KeyResource:
    """Key Resource component of the BMC"""
    def __init__(self, id, model_id, resource_name, description):
        self.id = id
        self.model_id = model_id
        self.resource_name = resource_name
        self.description = description

class KeyActivity:
    """Key Activity component of the BMC"""
    def __init__(self, id, model_id, activity_name, description):
        self.id = id
        self.model_id = model_id
        self.activity_name = activity_name
        self.description = description

class KeyPartnership:
    """Key Partnership component of the BMC"""
    def __init__(self, id, model_id, partner_name):
        self.id = id
        self.model_id = model_id
        self.partner_name = partner_name

class CostStructure:
    """Cost Structure component of the BMC"""
    def __init__(self, id, model_id, cost_name, amount):
        self.id = id
        self.model_id = model_id
        self.cost_name = cost_name
        self.amount = amount
