"""classes to initalize the variables"""
import datetime

USERS = []  # global variable for users.
FLAGS = []  # global variable for redflags


class User:
    """class for user registration"""

    def __init__(self, user_id, firstname, lastname, othernames, username, email, phonenumber, password):
          # initialise the variables for this class here
        self.user_id = user_id
        self.firstname = firstname
        self.lastname = lastname
        self.othernames = othernames
        self.username = username
        self.phonenumber = phonenumber
        self.email = email
        self.password = password
        self.registered_on = datetime.datetime.now()
        self.users_list = []

    def register(self, user_id, firstname, lastname, othernames, username, email, phonenumber, password):
        """ creating a new user and returns a  true if a user has been
        successfully registered and false if otherwise."""
        oldeusers = len(
            self.users_list)  # lets store the length of users_list before appending a new user.
        print(self.users_list != None)
        if self.users_list:
            for user in self.users_list:
                for vals in user.values():
                    if user_id not in vals:
                        # create the list below with precise indexing as illustrated below
                        # { user_id:[[0]= firstname, [1]= secondname, [2]=lastname,[3]othernames, [4] = username, [5] = phonenumber, [6] = email, [7] = password }
                        self.users_list.append(
                            {user_id: [firstname, lastname, othernames, username, phonenumber, email, password]})
                        if len(self.users_list) > oldeusers:
                            # 'user added' # user was created successfully.
                            return True
                        else:
                            return False  # user was not created.
                    else:
                        self.users_list.append(
                            {user_id: [firstname, lastname, othernames, username, phonenumber, email, password]})
                        return True
        else:
            self.users_list.append(
                {user_id: [firstname, lastname, othernames, username, phonenumber, email, password]})
            return True

    def checkUsernameExists(self, username):
        """checks whether username Exists before registering a new user and returns
        a boolean true if the username already exists and false if the username is not yet used."""
        # lets loop through this global users_list and append all usernames to list availUsernames
        availUsernames = []

        if USERS:
            for items in USERS:
                for values in items.values():
                    # index 4 holds our usernames by default.
                    availUsernames.append(values[4])
                    if username not in availUsernames:
                        return False
                    return True
        else:
            print(availUsernames)
            return False


class Redflag:
    """class for creating a redflag post """

    def __init__(self, flag_id, type, comment, location, media):
        self.flag_id = flag_id
        self.type = type
        self.comment = comment
        self.location = location
        self.media = media
        self.createdOn = datetime.datetime.now()
        self.redflag_list = []

    def create_redflag(self):
        """ posting a redflag. funtion returns true if the redflag has been created and false if redflag is not created."""
        global FLAGS
        result = False
        # length of redflag list before manipulation.
        oldflagListLength = len(FLAGS)
        # create the list below with precise indexing as illustrated below
        # [0] = user_id, [1] = type, [2] = comment, [3] = media, [4] = location, [5] =createdon [6] = created by
        FLAGS.append({[self.flag_id, self.type, self.comment,
                       self.location, self.media, self.createdOn]})

        if len(FLAGS) > oldflagListLength:
            # incase creating a redflag is successful return true.
            result = True
        else:
            result = False  # incase creating a redflag fails return False.
        return result

    @staticmethod
    def get_one_flag(flag_id):
        """function to check whether a business Exists or not. function return a boolean true if business exists and
        false if it does not exist."""
        index = None
        from views.users import loggedinuser
        global loggedinuser
        if loggedinuser:
            for x, y in enumerate(FLAGS, 0):
                for key, val in y.items():
                    if key == flag_id:
                        index = x
                        return index
        else:
            return index

    # @staticmethod
    # def update_flag(flag_id):
    #     """updating flag details. returns a index to update"""
    #     index = None
    #     global FLAGS
    #     redflag = []
    #     if FLAGS:
    #         for num, value in enumerate(FLAGS, 0):
    #             for key, val in value.items():
    #                 if key == flag_id:
    #                     index = num
    #                     redflag.append([index, val])
    #                     # FLAGS[index]={flag_id:[type,user_id,comment,email,location,createdOn,createdby]}
    #                     return redflag
    #     else:
    #         return redflag

    @staticmethod
    def delete_flag(flag_id):
        """ deleting a flag"""
        global loggedinuser
        index = None
        if FLAGS:
            for num, value in enumerate(FLAGS, 0):
                for key in value.items():
                    if key == flag_id:
                        index = num
                        return index
        else:
            return index

    # def get_all_flags(self):
    #     """returns a list of all flags registered."""
    #     global FLAGS
    #     if FLAGS:
    #         return FLAGS

    #     return None
