import datetime

USERS = []  # global variable for users.
FLAGS = []  # global variable for redflags


class User:
    """class for user registration"""

    def __init__(self, user_id, firstname, lastname, othernames, username, email, phonenumber, password, isAdmin):
          # initialise the variables for this class here
        self.user_id = user_id
        self.firstname = firstname
        self.lastname = lastname
        self.othernames = othernames
        self.username = username
        self.phonenumber = phonenumber
        self.email = email
        self.password = password
        self.isAdmin = isAdmin
        self.registered_on = datetime.datetime.now()
        self.users_list = []

    def register(self, user_id, firstname, lastname, othernames, username, email, phonenumber, password, isAdmin):
        """ creating a new user and returns a  true if a user has been
        successfully registered and false if otherwise."""
        oldUsersListLength = len(
            self.users_list)  # lets store the length of users_list before appending a new user.
        print(self.users_list != None)
        if self.users_list:
            for user in self.users_list:
                for vals in user.values():
                    if user_id not in vals:
                        # create the list below with precise indexing as illustrated below
                        # { user_id:[[0]= firstname, [1]= secondname, [2]=lastname,[3]othernames, [4] = username, [5] = phonenumber, [6] = email, [7] = password, [8] = isAdmin] }
                        self.users_list.append({user_id: [
                                               firstname, lastname, othernames, username, phonenumber, email, password, isAdmin]})
                        if len(self.users_list) > oldUsersListLength:
                            # 'user added' # user was created successfully.
                            return True
                        else:
                            return False  # user was not created.
                    else:
                        self.users_list.append({user_id: [
                                               firstname, lastname, othernames, username, phonenumber, email, password, isAdmin]})
                        return True
        else:
            self.users_list.append({user_id: [
                                   firstname, lastname, othernames, username, phonenumber, email, password, isAdmin]})
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
                        return False  # false will mean they dont exist
                    else:
                        return True  # this will mean they exist
        else:
            print(availUsernames)
            return False
  

class Redflag:
    """
    class for creating a redflag post 
    """

    def __init__(self, flag_id, type, description, location):
        self.flag_id = flag_id
        self.type = type
        self.description = description
        self.location = location
        self.createdOn = datetime.datetime.now()
        self.redflag_list = []

    def create_redflag(self):
        """ posting a redflag. funtion returns true if the redflag has been created and false 
        if redflag is not created."""
        global FLAGS
        result = False

        # length of redflag list before manipulation.
        oldflagListLength = len(FLAGS)
        # create the list below with precise indexing as illustrated below
        # [0] = user_id, [1] = type, [2] = description, [3] = email, [4] = location, [5] =createdon [6] = created by
        FLAGS.append({[self.flag_id,self.type, self.description,
                                    self.location, self.createdOn]})

        if len(FLAGS) > oldflagListLength:
            # incase creating a redflag is successful return true.
            result = True
        else:
            result = False  # incase creating a redflag failes return False.
        return result

    @staticmethod
    def get_specific_flag(flag_id):
       
        global FLAGS
        if FLAGS:
            for x, y in enumerate(FLAGS, 0):
                for key in y.items():
                    if key == flag_id:
                        index = x
                        return index
        else:
            return index

    @staticmethod
    def update_flag(flag_id):
        """updating flag details. returns a index to update"""
        index = None
        global FLAGS
        redflag = []
        if FLAGS:
            for x, y in enumerate(FLAGS, 0):
                for key, val in y.items():
                    if key == flag_id:
                        index = x
                        redflag.append([index, val])
                        # FLAGS[index]={flag_id:[type,user_id,description,email,location,createdOn,createdby]}
                        return redflag
        else:
            return redflag

    @staticmethod
    def delete_flag(flag_id):
        """ deleting a flag"""
        global FLAGS
        index = None
        if FLAGS:
            for x, y in enumerate(FLAGS, 0):
                for key in y.items():
                    if key == flag_id:
                        index = x
                        return index
        else:
            return index

    def get_all_flags(self):
        """returns a list of all flags registered."""
        global FLAGS
        if FLAGS:
            return FLAGS
        else:
            return None