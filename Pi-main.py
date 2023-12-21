import serial
import time
import csv
import os
import subprocess
import paramiko


def main():
	port = "/dev/ttyUSB0"
	baud_rate = 115200
	directory = "/home/caspberry/Documents/ToxiGuard/Patient_Data"
	
	while True:
		min_value = None
		max_value = None
		sum_value = 0
		count = 0

		try:
			with serial.Serial(port, baud_rate) as ser:
				print("Starting data collection...")
				start_time = time.strftime("%Y-%m-%d %H:%M:%S")
				while True:
					if ser.in_waiting:
						try:
							line = ser.readline().decode('utf-8').rstrip()
							print("Received:", line)
							
							value = float(line)
							min_value = value if min_value is None else min(min_value, value)
							max_value = value if max_value is None else max(max_value, value)
							sum_value += value
							count += 1

						except Exception as e:
							print("Error reading from serial port:", e)
					
					time.sleep(0.1)
					
					if count >= 20:
						break

		except Exception as e:
			print("An error occurred:", e)

		average_value = sum_value / count if count > 0 else 0

		os.makedirs(directory, exist_ok=True)

		csv_file = os.path.join(directory, "patient_data.csv")

		end_time = time.strftime("%Y-%m-%d %H:%M:%S")
		with open(csv_file, 'w', newline='') as file:
			writer = csv.writer(file)
			writer.writerow(['Start Timestamp', 'End Timestamp', 'Min Value', 'Max Value', 'Average Value'])
			writer.writerow([start_time, end_time, min_value, max_value, average_value])

		image_file = os.path.join(directory, "patient_image.jpg")
		command = f"libcamera-jpeg -t 1 -o {image_file}"

		process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		output, error = process.communicate()

		if error:
			print(f"Error occurred: {error.decode()}")
		else:
			print("Image captured successfully.")

		print("Data compilation and image capture completed.")


		def sftp_transfer_multiple_files(host, port, username, private_key_path, files, remote_directory):
			try:
				private_key = paramiko.RSAKey.from_private_key_file(private_key_path)

				ssh_client = paramiko.SSHClient()
				ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

				ssh_client.connect(hostname=host, port=port, username=username, pkey=private_key)

				sftp = ssh_client.open_sftp()

				for local_path in files:
					filename = os.path.basename(local_path)
					remote_path = os.path.join(remote_directory, filename)
					sftp.put(local_path, remote_path)
					print(f"File {filename} successfully transferred to {host}:{remote_path}")

				sftp.close()
				ssh_client.close()

			except Exception as e:
				print(f"Error occurred during SFTP transfer: {e}")

		sftp_transfer_multiple_files(
			host="192.168.137.103",
			port=22,
			username="aske1304",
			private_key_path="/home/caspberry/.ssh/id_rsa",
			files=[
				"/home/caspberry/Documents/ToxiGuard/Patient_Data/patient_data.csv",
				"/home/caspberry/Documents/ToxiGuard/Patient_Data/patient_image.jpg"
			],
			remote_directory="/home/aske1304/Patient_Data"
		)

if __name__ == "__main__":
    main()

