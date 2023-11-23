import logging
import subprocess
import threading

from .IO_module import setCPU, setUp, cleanUp, print_color
from .supabase_module import getJobId, downloadFile, upsertJob

# Info disabling
logging.getLogger("httpx").setLevel(logging.CRITICAL)
logging.getLogger("aiohttp").setLevel(logging.CRITICAL)
logging.getLogger("gql").setLevel(logging.CRITICAL)

# Create a flag to signal when the job is done
job_done = False
job_failed = False


def runJob():
    global job_done
    validated_input = setCPU()

    # Loop over to run the queue
    while True:
        # # Download the job
        # id = asyncio.run(retrieveQID())
        # Send the query and receive the response
        try:
            while True:
                id = getJobId()
                import time

                if id is None:
                    interval = 30  # Set the countdown interval to 30 seconds

                    for remaining in range(interval, 0, -1):
                        print(
                            f"   Currently there are no jobs due. Checking again in {remaining} seconds. Press Ctrl+C to exit.",
                            end="\r",
                        )
                        time.sleep(1)
                        # Clear the countdown timer
                        print(" " * len(f"{remaining} seconds"), end="\r")

                    print(" " * 90, end="\r")  # Clear any residual characters

                else:
                    break
        except KeyboardInterrupt:
            print_color("\nIVETTE CLI exited gracefully.", "34")
            raise SystemExit
        setUp()
        downloadFile(id)

        # Define the command as a list of arguments
        # Use the relative or absolute path to the input file in the subdirectory
        # Replace "subdirectory" and "input" with the actual subdirectory and file names
        command = [
            "rungms tmp/" + id + " 00 " + str(validated_input)
        ]  # The last one is ncores

        # Function to run the 'rungms' command and update the job_done flag

        def run_rungms():
            global job_done
            global job_failed
            with open("tmp/output.log", "w") as output_file:
                try:
                    # Run the 'rungms' command and wait for it to complete
                    subprocess.run(
                        command,
                        stdout=output_file,
                        stderr=subprocess.STDOUT,
                        shell=True,
                        check=True,  # This will raise an error if the command returns a non-zero exit code
                    )
                    upsertJob(id)
                    # client.execute(gql('''
                    #     query {
                    #         insertCalculation(jobId: "''' + id + '''", name: "output.log", status: "Failed")
                    #     }
                    #     ''')).get('insertCalculation')
                    job_done = True
                except subprocess.CalledProcessError as e:
                    if not e.returncode == -2:
                        upsertJob(id, "failed")
                        # client.execute(gql('''
                        #     query {
                        #         insertCalculation(jobId: "''' + id + '''", name: "output.log", status: "Failed")
                        #     }
                        #     ''')).get('insertCalculation')
                    cleanUp(id)
                    print(f"\n Command failed with exit code {e.returncode}.")
                    job_done = True
                    job_failed = True
                    raise SystemExit

        # Create a thread to run the 'rungms' command
        rungms_thread = threading.Thread(target=run_rungms)

        # Create an animated "Waiting" message using Braille characters
        waiting_message = "⣾⣷⣯⣟⡿⢿⣻⣽"  # Customize this as needed

        try:
            upsertJob(id, "in progress")
            print("Running Gamess Job")
            rungms_thread.start()  # Start the 'rungms' command thread
            while not job_done:
                for braille_char in waiting_message:
                    print(braille_char, end="\r", flush=True)
                    time.sleep(0.1)
            if job_failed: raise SystemExit
            rungms_thread.join()  # Wait for the 'rungms' command thread to finish
            cleanUp(id)
            print("Job completed successfully.")
            job_done = False
        except KeyboardInterrupt:
            upsertJob(id, "interrupted")
            cleanUp(id)
            print("\n Job interrupted.")
            raise SystemExit
