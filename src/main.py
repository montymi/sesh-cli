try:
    import argparse
    from controllers.appcontroller import AppController
    
    def main(args):
        try:
            ac = AppController(args)
            if ac.test() == 1:
                ac.run()
        except KeyboardInterrupt:
            return
        except Exception as e:
            print("Error configuring App Controller:", e)
            return

    if __name__ == "__main__":
        parser = argparse.ArgumentParser(description='Clerk Application')
        parser.add_argument('--ui', action='store_true', help='Start the application with a graphical user interface')
        parser.add_argument('--cli', action='store_true', help='Start the application with a terminal user interface')

        args = parser.parse_args()

        main(args)
except ModuleNotFoundError as e:
    print("Missing modules, try activating virtual environment if using one.")
