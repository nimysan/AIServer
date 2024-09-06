from flask import Blueprint, render_template_string
from flask_restx import Api, Resource, fields

bp = Blueprint('my_blueprint', __name__, url_prefix='/test')
api = Api(bp, version='1.0', title='Sample API',
          description='A simple API example using Flask-RESTx', doc='/doc/')

ns = api.namespace('operations', description='Resources operations')

operation_model = api.model('Operation', {
    'resource_type': fields.String(readonly=True, description='资源类型'),
    'resource_id': fields.String(required=True, description='资源唯一标识符'),
    'operation': fields.String(required=True, description='资源操作')
})

operations = []

@ns.route('/')
class OperationList(Resource):

    @ns.doc('add operation to specific resource')
    # @ns.expect(operation_model)
    @ns.marshal_with(operation_model, code=201)
    def post(self):
        '''发起一个针对某个资源的操作'''
        new_user = api.payload
        new_user['id'] = len(operations) + 1
        operations.append(new_user)
        return new_user, 201

    @ns.doc('get operation to specific resource')
    # @ns.expect(operation_model)
    @ns.marshal_with(operation_model, code=201)
    def get(self):
        '''发起一个针对某个资源的操作'''
        new_user = api.payload
        new_user['id'] = len(operations) + 1
        operations.append(new_user)
        return new_user, 201
