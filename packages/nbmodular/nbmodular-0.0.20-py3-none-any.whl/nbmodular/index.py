#|echo: false
import pandas as pd
def get_my_previous_variable():
    my_previous_variable = 100
    return my_previous_variable

def two_plus_three():
    a = 2
    b = 3
    c = a+b
    print (f'The result of adding {a}+{b} is {c}')
    return c

def add_100(my_previous_variable):
    my_previous_variable = my_previous_variable + 100
    print (f'The result of adding 100 to my_previous_variable is {my_previous_variable}')
    return my_previous_variable

def multiply_by_two(c):
    d = c*2
    print (f'Two times {c} is {d}')
    return d

def analyze(x):
    x = [1, 2, 3]
    y = [100, 200, 300]
    z = [u+v for u,v in zip(x,y)]
    product = [u*v for u, v in zip(x,y)]

def determine_approximate_age (name, birthday_year=2000):
    current_year = datetime.datetime.today().year
    approximate_age = current_year-birthday_year
    print (f'hello {name}, your approximate age is {approximate_age}')
    return approximate_age,current_year

def use_current_year(current_year):
    print (current_year)

# -----------------------------------------------------
# pipeline
# -----------------------------------------------------
def index_pipeline (test=False, load=True, save=True, result_file_name="index_pipeline"):
    """Pipeline calling each one of the functions defined in this module."""
    
    # load result
    result_file_name += '.pk'
    path_variables = Path ("index") / result_file_name
    if load and path_variables.exists():
        result = joblib.load (path_variables)
        return result

    my_previous_variable = get_my_previous_variable ()
    c = two_plus_three ()
    my_previous_variable = add_100 (my_previous_variable)
    d = multiply_by_two (c)
    analyze (x)
    approximate_age, current_year = determine_approximate_age (name, birthday_year)
    use_current_year (current_year)

    # save result
    result = Bunch (d=d,current_year=current_year,c=c,approximate_age=approximate_age,my_previous_variable=my_previous_variable)
    if save:    
        path_variables.parent.mkdir (parents=True, exist_ok=True)
        joblib.dump (result, path_variables)
    return result

