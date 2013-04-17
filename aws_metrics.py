#!/usr/bin/python


class AWSMetrics:
    #this is the main class which is called to get all the metrics of the given account
    EC2_TYPES = {	"m1.small" : {
			"compute_units" : 1,
			"cores" : 1,
			"gpus" : 0,
			"ramMB" : 1700,
			"storageGB" : [10, 160],
			"i/o" : "moderate",
			"ebs_optimized_iopsMbps" : 0,
			"arch" : [32,64]},
		    "m1.medium" : {
			"compute_units" : 2,
			"cores" : 1,
			"gpus" : 0,
			"ramMB" : 3750,
			"storageGB" : [10, 410],
			"i/o" : "moderate",
			"ebs_optimized_iopsMbps" : 0,
			"arch" : [32,64]},
		    "m1.large" : {
			"compute_units" : 4,
			"cores" : 2,
			"gpus" : 0,
			"ramMB" : 7500,
			"storageGB" : [10, 420, 420],
			"i/o" : "high",
			"ebs_optimized_iopsMbps" : 500,
			"arch" : [64]},
		    "m1.xlarge" : {
			"compute_units" : 8,
			"cores" : 4,
			"gpus" : 0,
			"ramMB" : 15000,
			"storageGB" : [10, 420, 420, 420, 420],
			"i/o" : "high",
			"ebs_optimized_iopsMbps" : 1000,
			"arch" : [64]},
		    "m3.xlarge" : {
			"compute_units" : 13,
			"cores" : 4,
			"gpus" : 0,
			"ramMB" : 15000,
			"storageGB" : [],
			"i/o" : "moderate",
			"ebs_optimized_iopsMbps" : 0,
			"arch" : [64]},
		    "m3.2xlarge" : {
			"compute_units" : 26,
			"cores" : 8,
			"gpus" : 0,
			"ramMB" : 30000,
			"storageGB" : [],
			"i/o" : "high",
			"ebs_optimized_iopsMbps" : 0,
			"arch" : [64]},
		    "t1.micro" : {
			"compute_units" : 2,
			"cores" : 1,
			"gpus" : 0,
			"ramMB" : 613,
			"storage" : [],
			"i/o" : "low",
			"ebs_optimized_iopsMbps" : 0,
			"arch" : [32,64]},
		    "c1.medium" : {
			"compute_units" : 5,
			"cores" : 2,
			"gpus" : 0,
			"ramMB" : 1700,
			"storageGB" : [10, 350],
			"i/o" : "moderate",
			"ebs_optimized_iopsMbps" : 0,
			"arch" : [32,64]},
		    "c1.xlarge" : {
			"compute_units" : 20,
			"cores" : 8,
			"gpus" : 0,
			"ramMB" : 7000,
			"storageGB" : [10, 420, 420, 420, 420],
			"i/o" : "high",
			"ebs_optimized_iopsMbps" : 0,
			"arch" : [64]},
		    "m2.xlarge" : {
			"compute_units" : 6.5,
			"cores" : 2,
			"gpus" : 0,
			"ramMB" : 17100,
			"storageGB" : [10, 420],
			"i/o" : "moderate",
			"ebs_optimized_iopsMbps" : 0,
			"arch" : [64]},
		    "m2.2xlarge" : {
			"compute_units" : 13,
			"cores" : 4,
			"gpus" : 0,
			"ramMB" : 34200,
			"storageGB" : [10, 840],
			"i/o" : "high",
			"ebs_optimized_iopsMbps" : 0,
			"arch" : [64]},
		    "m2.4xlarge" : {
			"compute_units" : 26,
			"cores" : 8,
			"gpus" : 0,
			"ramMB" : 68400,
			"storageGB" : [10, 840, 840],
			"i/o" : "high",
			"ebs_optimized_iopsMbps" : 1000,
			"arch" : [64]},
		    "cc1.4xlarge" : {
			"compute_units" : 33.5,
			"cores" : 16,
			"gpus" : 0,
			"ramMB" : 23000,
			"storageGB" : [10, 840, 840],
			"i/o" : "very high",
			"ebs_optimized_iopsMbps" : 0,
			"arch" : [64]},
		    "cc2.8xlarge" : {
			"compute_units" : 88,
			"cores" : 32,
			"gpus" : 0,
			"ramMB" : 60500,
			"storageGB" : [10, 840, 840, 840, 840],
			"i/o" : "very high",
			"ebs_optimized_iopsMbps" : 0,
			"arch" : [64]},
		    "cg1.4xlarge" : {
			"compute_units" : 33.5,
			"cores" : 16,
			"gpus" : 2,
			"ramMB" : 22000,
			"storageGB" : [10, 840, 840],
			"i/o" : "very high",
			"ebs_optimized_iopsMbps" : 0,
			"arch" : [64]},
		    "hi1.4xlarge" : {
			"compute_units" : 35,
			"cores" : 16,
			"gpus" : 0,
			"ramMB" : 60500,
			"storageGB" : [10, 1024, 1024],
			"i/o" : "very high",
			"ebs_optimized_iopsMbps" : 0,
			"arch" : [64]}
		}
    api_key = None
    api_secret = None
    ec2_conn = None
    cloudwatch_conn = None

    def __init__(self, api_key=None, api_secret=None):
	"""This is the initialization method of the class
	this will require API Key and Secret of the account to initialise
	"""
	if api_key and api_secret:
	    self.api_key = api_key
	    self.api_secret = api_secret
	else:
	    print "For initialization API Key and API Secret is required"
	    return None

    def get_ec2_conn(self):
	"""This function returns the EC2 connection object to the account

	"""
	if self.ec2_conn:
	    return self.ec2_conn
	else:
	    from boto.ec2.connection import EC2Connection
	    try:
		self.ec2_conn = EC2Connection(self.api_key, self.api_secret)
		return self.ec2_conn
	    except:
		print "Unable to get the connection, wrong API KEY and SECRET"
		return None

    def get_cloudwatch_conn(self):
	"""This function returns the Cloudwatch connection object
	"""
	if self.cloudwatch_conn:
	    return self.cloudwatch_conn
	else:
	    import boto
	    try:
		self.cloudwatch_conn = boto.connect_cloudwatch(self.api_key, self.api_secret)
		return self.cloudwatch_conn
	    except:
		print "Unable to get the cloudwatch connection, Wrong API KEY, SECRET combination"
		return None

    def get_current_instances(self):
	try:
	    conn = self.get_ec2_conn()
	    reservations = conn.get_all_instances()
	    instances = [i for r in reservations for i in r.instances]
	    for i in instances:
		print "InstanceId:%s, Instance Type: %s, Launch Time: %s, Ip Address: %s, Public DNS Name: %s" %(i.id, i.instance_type, i.launch_time, i.ip_address, i.public_dns_name)
	except Exception, e:
	    print e

    def get_network_op(self):
	dimensions = {}
	statistics = ['Average']
	conn = self.get_ec2_conn()
	reservations = conn.get_all_instances()
	instances = [i for r in reservations for i in r.instances]
	for i in instances:
	    cloudwatch_conn = self.get_cloudwatch_conn()
	    import datetime
	    end = datetime.datetime.now()
	    start = end - datetime.timedelta(hours = 12)
	    dimensions['InstanceId'] = i.id
	    metric_name = 'NetworkIn'
	    datapoints = cloudwatch_conn.get_metric_statistics(900, start, end, metric_name, 'AWS/EC2', statistics, dimensions,  'Percent')
	    for y in datapoints:
		print "%s: %s %s" %(y['Timestamp'].strftime("%d %b %Y, %H:%M"), y['Average'], y['Unit'])

    def get_cpu_usage(self):
	dimensions = {}
	statistics = ['Average']
	conn = self.get_ec2_conn()
	reservations = conn.get_all_instances()
	instances = [i for r in reservations for i in r.instances]
	for i in instances:
	    cloudwatch_conn = self.get_cloudwatch_conn()
	    import datetime
	    end = datetime.datetime.now()
	    start = end - datetime.timedelta(hours = 12)
	    dimensions['InstanceId'] = i.id
	    metric_name = 'CPUUtilization'
	    datapoints = cloudwatch_conn.get_metric_statistics(900, start, end, metric_name, 'AWS/EC2', statistics, dimensions,  'Byte')
	    for y in datapoints:
		print "%s: %s %s" %(y['Timestamp'].strftime("%d %b %Y, %H:%M"), y['Average'], y['Unit'])

    def get_volumes_attached(self):
	conn = self.get_ec2_conn()
	volumes = conn.get_all_volumes()
	for x in volumes:
	    print "VolumeId:%s, Volume Size:%s GB, Volume region: %s, Status: %s" %(x.id, x.size, x.region, x.status)

    def get_disk_usage(self):
	dimensions = {}
	statistics = ['Sum']
	conn = self.get_ec2_conn()
	volumes = conn.get_all_volumes()
	for x in volumes:
	    cloudwatch_conn = self.get_cloudwatch_conn()
	    import datetime
	    end = datetime.datetime.now()
	    start = end - datetime.timedelta(hours = 12)
	    dimensions['VolumeId'] = x.id
	    metric_name = 'VolumeWriteBytes'
	    datapoints = cloudwatch_conn.get_metric_statistics(900, start, end, metric_name, 'AWS/EBS', statistics, dimensions,  'Bytes')
	    for y in datapoints:
		print "%s: %s %s" %(y['Timestamp'].strftime("%d %b %Y, %H:%M"), y['Sum'], y['Unit'])

	

	    
	
if __name__ == "__main__":
    ACCESS_KEY='YOUR AWS KEY'
    SECRET='YOUR AWS SECRET'
    aws_object = AWSMetrics(ACCESS_KEY, SECRET)
    print "Gettings all the servers which are present in your account "
    aws_object.get_current_instances()
    print "\n\n\n\nGettings the CPU Usages of the servers which are running"
    aws_object.get_cpu_usage()
    print "\n\n\n\nGetting the details of the Volumes(Disk) that are attached to the servers:"
    aws_object.get_volumes_attached()
    print "\n\n\n\nGetting the disk usages of the volumes now...:"
    aws_object.get_disk_usage()
    print "\n\n\n\nGetting the network input on the servers:"
    aws_object.get_network_op()
