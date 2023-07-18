from Swarm import Swarm

def main ():
    try:
        instance = Swarm()
        instance.execute()
    except Exception as error:
        print(f"Error: {error}")

if __name__ == "__main__":
    main()