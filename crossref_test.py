import click
import json
from habanero import Crossref
cr = Crossref()


@click.command()
@click.option('--stxt', prompt='What are you looking for?', help='Title, author, DOI, etc.')
def search_paper(stxt):
    click.echo(f"Now we search for the txt in crossref:  {stxt}!")
    x = cr.works(query=stxt)
    papers = []
    # now we fetch the essential data from each item
    for npaper in range(x['message']['items-per-page']):
        print(npaper)
        xitem = x['message']['items'][npaper]
        paper = {}
        paper['doi'] = xitem['DOI']
        xauthors = xitem['author']
        paper['au1'] = xauthors[0]['given'] + " " + xauthors[0]['family']
        paper['title'] = xitem['title'][0]
        try:
            paper['journal'] = xitem['container-title'][0]
        except:
            paper['journal'] = 'NA'
        try:
            paper['year'] = xitem['published']['date-parts'][0][0]
        except:
            paper['year'] = 'NA'
        # put all the information into a list of dicts
        papers.append(paper)
    # debug
    print(json.dumps(papers, indent=4))


# # query
# x = cr.works(query = "Elementary Andreev processes in a driven superconductor–normal metal contact" )


# # all the information are stored in x['message']
# for keys in x.keys():
#   print(keys)

# # we get x['message']['items-per-page'] results
# for keys in x['message'].keys():
#   print(keys)

# by default, return the first 20 results
# n_results = x['message']['items-per-page']


# # now we fetch the essential data from each item
# for npaper in range(x['message']['items-per-page']):
#   print(npaper)
#   xitem = x['message']['items'][npaper]
#   paper = {}
#   paper['doi'] = xitem['DOI']
#   xauthors = xitem['author']
#   paper['au1'] = xauthors[0]['given'] + " " + xauthors[0]['family']
#   paper['title'] = xitem['title'][0]
#   try:
#     paper['journal'] = xitem['container-title'][0]
#   except:
#     paper['journal'] = 'NA'
#   try:
#     paper['year'] = xitem['published']['date-parts'][0][0]
#   except:
#     paper['year'] = 'NA'
#   # debug
#   print(json.dumps(paper, indent=4))


# xdoi = x['message']['items'][0]['DOI']
# xtitle = x['message']['items'][0]['title'][0]
# xauthors = x['message']['items'][0]['author']
# xjournal = x['message']['items'][0]['container-title'][0]
# xvolume = x['message']['items'][0]['volume']
# xpage = x['message']['items'][0]['page'].split("-")[0]
# xyear = x['message']['items'][0]['published']['date-parts'][0][0]
# xmonth = x['message']['items'][0]['published']['date-parts'][0][1]
# # x['message']['items'][0]['reference']

# print(xdoi)
# print(xtitle)
# print(xauthors)
# print(xjournal)
# print(xvolume)
# print(xpage)
# print(xyear)

# paper = {}
# paper['doi'] = xdoi     # we use doi as the primary key
# paper['title'] = xtitle
# paper['journal'] = xjournal
# paper['year'] = xyear
# paper['au1'] = xauthors[0]['given'] + " " + xauthors[0]['family']


# # find all authors
# for au in xauthors:
#   print(au['given'])
#   print(au['family'])
if __name__ == '__main__':
    search_paper()
