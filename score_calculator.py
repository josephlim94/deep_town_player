

def print_report(item_list, total_GPS, iterations, virtual_time_passed):
    '''Print a nicely formatted report of item list'''

    complete_report_string = ""

    report_header_format = '''
Total GPS: {total_gps}
Iterations: {iterations}
Virtual Time Passed: {virtual_time_passed}
'''

    report_item_format = '''
Item number: {number}
Name: {name}
Price: {price}
Period: {period}
Amount Produced: {amount_produced}
Rate: {rate}
Real Rate: {real_rate}
GPS: {item_gps}
'''

    report_source_format = '''
    Source number: {number}
    Name: {name}
    Amount Needed: {amount_needed}
    Price: {price}
    Period: {period}
    Rate: {rate}
    Real Rate: {real_rate}
'''

    report_header_data = dict()
    report_header_data["total_gps"] = total_GPS
    report_header_data["iterations"] = iterations
    report_header_data["virtual_time_passed"] = virtual_time_passed

    complete_report_string += report_header_format.format(**report_header_data)

    x = 1
    for item in item_list:
        report_item_data = dict()
        report_item_data["number"] = x
        x += 1
        report_item_data["name"] = item.name
        report_item_data["price"] = item.price
        report_item_data["period"] = item.prod_period
        report_item_data["amount_produced"] = item.prod_amount
        report_item_data["rate"] = item.rate
        report_item_data["real_rate"] = item.prod_rate
        report_item_data["item_gps"] = item.GPS

        complete_report_string += report_item_format.format(**report_item_data)
        if item.source_list:
            complete_report_string += "\n    Sources required:\n"
        else:
            complete_report_string += "\n    No source required\n"

        y = 1
        for source in item.source_list:
            report_source_data = dict()
            report_source_data["number"] = y
            y += 1
            report_source_data["name"] = source.name
            report_source_data["price"] = 0
            report_source_data["period"] = 0
            report_source_data["amount_needed"] = source.amount
            report_source_data["rate"] = 0
            report_source_data["real_rate"] = 0

            complete_report_string += report_source_format.format(**report_source_data)

    print(complete_report_string)


class ItemData:
    def __init__(self, item):
        self.item = item
        self.name = item.name
        self.prod_period = 0
        self.prod_amount = item.amount
        self.prod_rate = 0.0
        self.rate = item.rate
        self.price = item.price
        self.source_list = item.source_list

        self.calculation_required = True
        self.GPS = 0.0


def get_source_rate(item_list, source):
    ''' Get the real source production rate
    Which are dependant on at least the following variables:
        - if it is being produced
        - real production rate of the source
    '''

    # First thing is see if it is produced
    for item in item_list:
        if item.name == source.name:
            # Source is in list of production
            # Now check if it is actually being produced
            if item.calculation_required:
                # Needs more iteration
                # Can't calculate source production rate yet
                return 0
            else:
                return item.prod_rate
    else:
        # Source is not in the list
        print(item.name + "is not in the production list.")
        return None


def calculate_score(input):
    # values to be calculated
    total_GPS = 0
    iteration = 0
    virtual_time_passed = 0
    complete = False
    item_list = list()

    # Put all production items into a wrapper
    for item in input:
        item_data = ItemData(input[item])
        item_list.append(item_data)

    while(not complete):
        iteration += 1
        # raise exception if iteration is more than 20 for debugging purposes
        if iteration > 20:
            raise Exception("Too many iterations. It's taking too long")

        for item in item_list:
            if (not item.calculation_required):
                # item have already completed calculation
                continue

            source_time_required_list = list()
            # Loop through all sources needed for item production
            for source in item.source_list:
                source_rate = get_source_rate(item_list, source)
                if (source_rate == 0):
                    # source rate is zero, meaning not yet created in dataset
                    break
                elif (source_rate == None):
                    # source rate is None, meaning not possible to create
                    item.calculation_required = False
                    break
                source_time_required = source.amount / source_rate
                source_time_required_list.append(source_time_required)
            else:
                # All sources required are ready
                # Calculated value
                if source_time_required_list:
                    item.prod_period = max(source_time_required_list)
                    item.prod_rate = float(item.prod_amount) / item.prod_period
                else:
                    item.prod_period = 1
                    item.prod_rate = item.rate
                item.GPS = item.price * item.prod_rate
                # Calculation for this item is complete
                item.calculation_required = False

        # Check if calculation is complete
        for item in item_list:
            if item.calculation_required is True:
                break
        else:
            # All item calculations are complete
            complete = True

    # Calculate total GPS
    for item in item_list:
        total_GPS += item.GPS
        if item.prod_period > virtual_time_passed:
            virtual_time_passed = item.prod_period

    # Print report for debugging purposes
    print_report(item_list, total_GPS, iteration, virtual_time_passed)

    return total_GPS
