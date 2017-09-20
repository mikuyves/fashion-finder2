from finder import Fashion, print_result


url = input('Enter Url: ')
f = Fashion(url)
f.parse()
print_result(f)
