from SiteScanner.Scanner import SiteScanner, websites




justpaste = websites['justpaste']
instagram = websites['instagram']
ibb = websites['ibb']

justpaste.StartScan(thread = True)
instagram.StartScan(thread = True)
ibb.StartScan(thread = True)

SiteScanner.handle_termination([
    justpaste,
    instagram,
    ibb,
])
