from .keys import KineticKeys

class KineticAuth:

    def __init__(self):
        pass

    def is_function(self, param):
        return callable(param)

    ###############################################################################
    # Generate an API Key for a user.
    ###############################################################################
    def create_api_key(self, j, public_len=8, private_len= 32, pre_trigger=None, post_trigger=None):

        # j: is a dict object with any data the application wants to
        #    pass in.

        if isinstance(j, dict):
            # Processing the external pre_trigger function.
            # This function allows users to access some external validation function.
            # must return at least {"error_code": "0"} to continue.
            if pre_trigger is None:
                tmp = {"error_code": "0", "error_msg": "",  "data": ""}
                pass
            else:
                if self.is_function(pre_trigger):
                    tmp = pre_trigger(j)
                    if tmp is None:
                        tmp = {"error_code": "0"}

            if 'error_code' in tmp:
                if tmp['error_code'] == "0":
                    if 'data' in tmp:
                        if isinstance(tmp['data'], dict):
                            data = tmp['data']
                            for key in data:
                                j[key] = data[key]
                else:
                    return {"error_code": "9999", "error_msg": "Pre-Trigger Failed", "data": tmp}

            private_key = KineticKeys.make_random_key(private_len)
            public_key = KineticKeys.make_random_key(public_len)
            j['public_key'] = public_key
            j['private_key'] = private_key
            if post_trigger is None:
                return {"error_code": "0", "error_msg": "", "data": j}
            else:
                tmp2 = post_trigger(j)
                if 'error_code' in tmp2:
                    if tmp2['error_code'] == "0":
                        pass
                    else:
                        return {"error_code": "9999", "error_msg": "Pre-Trigger Failed", "data": tmp2}
        else:
            return {"error_code": "5504", "error_msg": "First Parameter must be a dictionary", "data": {}}
