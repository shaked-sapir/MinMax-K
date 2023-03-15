import openpyxl
import os


def toxl(DataRow):
    # create a new workbook and select the active worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    # write data to cells
    worksheet['A1'] = 'K'
    worksheet['B1'] = 'minmaxk_depth'
    worksheet['C1'] = 'alpha_beta_depth'
    worksheet['D1'] = 'nodes_white_avg'
    worksheet['E1'] = 'nodes_white_sum'
    worksheet['F1'] = 'nodes_black_avg'
    worksheet['G1'] = 'nodes_black_sum'
    worksheet['H1'] = 'time_white_avg'
    worksheet['I1'] = 'time_white_sum'
    worksheet['J1'] = 'time_black_avg'
    worksheet['K1'] = 'time_black_sum'
    worksheet['L1'] = 'sim_result'
    worksheet['M1'] = 'expected_result'
    worksheet['N1'] = 'alg_white'
    worksheet['O1'] = 'alg_black'
    worksheet['P1'] = 'num_turns'
    worksheet['Q1'] = 'fen_position'

    index=2
    for row in DataRow:
        worksheet['A'+ str(index)] = row[0]
        worksheet['B'+ str(index)] = row[1]
        worksheet['C'+ str(index)] = row[2]
        worksheet['D'+ str(index)] = row[3]
        worksheet['E'+ str(index)] = row[4]
        worksheet['F'+ str(index)] = row[5]
        worksheet['G'+ str(index)] = row[6]
        worksheet['H'+ str(index)] = row[7]
        worksheet['I'+ str(index)] = row[8]
        worksheet['J'+ str(index)] = row[9]
        worksheet['K'+ str(index)] = row[10]
        worksheet['L'+ str(index)] = row[11]
        worksheet['M'+ str(index)] = row[12]
        worksheet['N'+ str(index)] = row[13]
        worksheet['O'+ str(index)] = row[14]
        worksheet['P'+ str(index)] = row[15]
        worksheet['Q'+ str(index)] = row[16]

        index+=1


    # save the workbook
    workbook.save('therd_Result.xlsx')



    # worksheet['A' + str(index)] = row.K
    # worksheet['B' + str(index)] = row.minmaxk_depth
    # worksheet['C' + str(index)] = row.alpha_beta_depth
    # worksheet['D' + str(index)] = row.nodes_white_avg
    # worksheet['E' + str(index)] = row.nodes_white_sum
    # worksheet['F' + str(index)] = row.nodes_black_avg
    # worksheet['G' + str(index)] = row.nodes_black_sum
    # worksheet['H' + str(index)] = row.time_white_avg
    # worksheet['I' + str(index)] = row.time_white_sum
    # worksheet['G' + str(index)] = row.time_black_avg
    # worksheet['K' + str(index)] = row.time_black_sum
    # worksheet['L' + str(index)] = row.sim_result
    # worksheet['M' + str(index)] = row.expected_result
    # worksheet['N' + str(index)] = row.alg_white
    # worksheet['O' + str(index)] = row.alg_black
    # worksheet['P' + str(index)] = row.num_turns
    # worksheet['Q' + str(index)] = row.fen_position


    # print(os.getcwd())
    # load excel file
    # workbook = load_workbook(filename="csv/Email_sample.xlsx")
    # open workbook
    # sheet = workbook.active
    # modify the desired cell
    # sheet["A1"] = "Full Name"
    # save the file
    # workbook.save(filename="csv/output.xlsx")
