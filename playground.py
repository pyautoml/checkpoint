from models.checkpoint_model import checkpoint, Checkpoint


# ----------------------------------
# Example functions in your code
# ----------------------------------
@checkpoint([3, 1, 2])
def calculate(a: int, b: int) -> int:
    return a + b

@checkpoint([5])
def say_hello() -> None:
    print("Hello!")

@checkpoint([4])
def greet(name: str) -> None:
    print(f"Hi, {name}!")


# -----------------------------------------
# Helper functions to present use cases
# -----------------------------------------
def registered_data() -> None:
    for index, i in enumerate(Checkpoint._call_stack):
        print(index, i)
    print()


def proper_calls() -> None:
    """This is a successful usage of Checkpoint class with properly registered and called methods."""    
    calculate(1, 2)
    calculate(3, 4)
    calculate(5, 6)
    greet("John")
    say_hello()

def inproper_calls() -> None:
    """This is an wrong usage of Checkpoint class with inproper calling order methods."""    
    calculate(1, 2)
    say_hello()
    calculate(3, 4)
    calculate(5, 6)
    greet("John")

def save_checkpoints(option: str = "basic"):
    # ---------------------------------------------------
    # Basic checkpoint history save.
    # Save file with a generic name using a timestamp.
    # ---------------------------------------------------
    if option == "basic":
        Checkpoint.save_track(autocreate_path=True)

    # ------------------------------------------------
    # Checkpoint history save groupped by method name.
    # Missing .json suffix is added.
    # ------------------------------------------------
    elif option == "grouped":
        Checkpoint.save_track(groupby_key="name", autocreate_path=True, file="./groupped_by_name") 

    # -------------------------------------------------
    # Checkpoint history save groupped by method name.
    # Missing 'data' directory is created
    # -------------------------------------------------
    elif option == "to_directory":
        Checkpoint.save_track(groupby_key="name", autocreate_path=True, file="./data/groupped_by_name.json") 
    else:
        Checkpoint.save_track(autocreate_path=True)



def use_case(option: str):
    option: str = option.lower()
    if option == "success":
        proper_calls()

        # ----------------------------------------------------------------------
        # Uncomment to check how the data is stored by the Checkpoint class.
        # ----------------------------------------------------------------------
        # registered_data()    

        # -----------------------------------------------------------
        # Save trackin hhistory as local json file. 
        # Comment/uncomment different options in save_checkpoints()
        # Options: basic, groupped, to_directory
        # -----------------------------------------------------------
        # save_checkpoints(option="basic")
    else:
        try:
            inproper_calls()
        except IndexError as e:
            print(f"""This is how inproper order should behave. Raising an error is expected. 
                Error message:\n\n--- ERROR ---\n{e}\n{12*'-'}"""
            )

def main():
    use_case(option="success")  # enter any other string to invoke unsuccessful use case


if __name__ == "__main__":
    main()
