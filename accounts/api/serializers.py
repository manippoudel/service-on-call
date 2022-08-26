from rest_framework import serializers
from accounts.models import Account


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    
    class  Meta():
        model       = Account
        fields      = ['email', 'username', 'fname', 'lname', 'contact_no', 'bike_no', 'password', 'password2']
        extra_kwargs = {
            'password':{'write_only': True}
        }
        
    def save(self):
        account = Account(
            email               = self.validated_data['email'],
            username            = self.validated_data['username'],
            bike_no             = self.validated_data['bike_no'],
            fname               = self.validated_data['fname'],
            lname               = self.validated_data['lname'],
            contact_no          = self.validated_data['contact_no'],
            )
        password        = self.validated_data['password']
        password2        = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({'password': 'Password Must Match'})
        account.set_password(password)
        account.save()
        return account
    
    

class AccountProrpertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Account
        fields  = ['pk', 'email', 'username', 'fname', 'lname', 'contact_no', 'bike_no']
        
class ChangePasswordSerializer(serializers.Serializer):
    
	old_password 				= serializers.CharField(required=True)
	new_password 				= serializers.CharField(required=True)
	confirm_new_password 		= serializers.CharField(required=True)