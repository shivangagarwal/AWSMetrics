AWSMetrics
Connects to AWS, and gets the basic monitoring metrics from Cloudwatch and Server and Disk Volume information

Usage: For initialization of the class Your AWS KEY and AWS SECRET wll be reqired

for initialization:  aws_object = AWSMrtics(AWS_KEY, AWS_SECRET)

to get all the current instances: aws_object.get_current_instances()

to get cpu usages for the past 12 hours:  aws_object.get_cpu_usage()

getting the details of the Disk volumes: aws_object.get_volumes_attached()

getting disk usages of the volumes for the past 12 hours: aws_object.get_disk_usage

getting network output of the servers: aws_object.get_network_op()
