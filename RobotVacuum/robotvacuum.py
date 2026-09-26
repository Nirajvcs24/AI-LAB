def reqFunc(position, cleaned):

    pos_index = 0 if position == "left" else 1
    
    if cleaned[pos_index]:
        position = "right" if position == "left" else "left"
        print(f"Position was already cleaned. Moving to: {position}")
    else:
        # Clean the current position
        print(f"Cleaning {position}...")
        cleaned[pos_index] = True
        
    return position, cleaned

def runVacuumRobot():
    cleaned = [False, False]
    
    position = "left" 
    
    step = 1
    while not (cleaned[0] and cleaned[1]):
        print(f"\n--- Step {step} ---")
        print(f"Current status -> Left clean: {cleaned[0]}, Right clean: {cleaned[1]}")
        
        position, cleaned = reqFunc(position, cleaned)
        step += 1
        
    print("\Both sides have been successfully cleaned! Vacuum stopping.")

if __name__ == "__main__":
    runVacuumRobot()
