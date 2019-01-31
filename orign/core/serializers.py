from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from .models import Client, House, Vehicle, RiskScore
from .models import ACTUAL_YEAR


class HousesSerializer(serializers.ModelSerializer):

    class Meta:
        model = House
        fields = "__all__"
        read_only_field = 'client'


class VehiclesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):

    class Meta:

        model = Client
        fields = ('id', 'age', 'dependents', 'income', 'marital_status')
        #fields = "__all__"
        read_only_fields = ('risk_scores', 'vehicles', 'houses')


class ClientUpdateSerialzier(WritableNestedModelSerializer):

    houses = HousesSerializer(many=True)
    vehicles = VehiclesSerializer(many=True)

    class Meta:
        model = Client
        fields = ('houses', 'vehicles', 'risk_questions')


class UpdatedClientSerializer(WritableNestedModelSerializer):

    houses = HousesSerializer(many=True)
    vehicles = VehiclesSerializer(many=True)

    class Meta:
        model = Client
        fields = ('id', 'age', 'dependents', 'income', 'marital_status', 'houses', 'vehicles', 'risk_questions')


class RiskScoreSerializer(WritableNestedModelSerializer):

    client = UpdatedClientSerializer(read_only=False)
    #Working to set vehicle and house as dicts
    auto = serializers.PrimaryKeyRelatedField(read_only=True)
    home = serializers.PrimaryKeyRelatedField(read_only=True)
    life = serializers.CharField(max_length=50, read_only=True)
    umbrella = serializers.CharField(max_length=50, read_only=True)
    disability = serializers.CharField(max_length=50, read_only=True)

    class Meta:
        model = RiskScore
        fields = ('client', 'auto', 'disability', 'home', 'life', 'umbrella',)
        read_only_fields = ('score', 'risk_scores', 'vehicles', 'houses', 'client')

    #restore a primitive datatype into its internal python representation
    def to_internal_value(self, data):

        values = super().to_internal_value(data)
        #acess the nested serializer fields values
        age = data.get('client', dict()).get('age')
        income = data.get('client', dict()).get('income')
        dependents = data.get('client', dict()).get('dependents')
        marital_status = data.get('client', dict()).get('marital_status')
        risk_questions = data.get('client', dict()).get('risk_questions')
        auto = data.get('client', dict()).get('vehicles')
        home = data.get('client', dict()).get('houses')

        #Working to alter values when update on POST method!
        #lines = ['auto', 'home', 'life', 'umbrella', 'disability']
        score = [0, 0, 0, 0, 0]

        def base_score(var):
            res_sum = var.count('1')
            values['base_score'] = risk_questions.count('1')

        def deduct_line_points(point):
            for i in range(len(score)):
                score[i] -= point

        #Manipulating list (houses)
        for key in home:
            ownership_status = key['ownership_status']
            self.home_pk = key['key']
            if len(home) <= 1:
                score[1] += 1
            if ownership_status == "mortgaged":
                score[1] += 1
                score[4] += 1

        #Manipulating list (vehicle)
        for key in auto:
            year = key['year']
            if len(auto) <= 1:
                score[0] += 1
            self.vehicle_pk = key['key']
            self.list_vehicle = (self.vehicle_pk, year)

            if year >= (int(ACTUAL_YEAR.year) - 5):
                score[0] += 1

        if age < 30:
            deduct_line_points(2)
        elif age in range(30, 40):
            deduct_line_points(1)
        elif income > 200:
            deduct_line_points(1)
        elif dependents >= 1:
            score[2] += 1
            score[4] += 1
        elif marital_status == 'married':
            score[2] += 1
            score[4] -= 1

        def calc_res(line):

                if score[line] <= 0:
                    return 'economic'

                if 1 <= score[line] <= 2:
                    return 'regular'

                if score[line] >= 3:
                    return 'responsible'
                else:
                    return 'NaN'

        list_auto = []
        for key in auto:
            if key in auto:
                key = key['key']
                list_auto.append({'key': key, 'value': calc_res(0)})
        values['auto'] = list_auto
        list_home = []
        for key in home:
            if key in home:
                key = key['key']
                list_home.append({'key': key, 'value': calc_res(1)})
        values['home'] = list_home

        for data in score:

            values['life'] = calc_res(2)
            values['disability'] = calc_res(3)
            values['umbrella'] = calc_res(4)

            if income == 0:
                values['disability'] = "ineligible"
            if auto is 'null':
                values['auto'] = "ineligible"
            if home is 'null':
                values['home'] = "ineligible"

            elif age > 60:
                values['disability'] = "ineligible"
                values['life'] = "ineligible"

            if ('economic' in str(data)) or (values['umbrella'] == 'economic'):
                values['umbrella'] = 'eligible'

        return values
