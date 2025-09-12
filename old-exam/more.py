

/*************  ✨ Windsurf Command 🌟  *************/
def main():
    # add_gdrive_folder_icon_recursive(all_path, recursive=True)
    remove_filename(all_path, "desktop.ini", recursive=True)
    files = get_files(all_path, file_extension="pdf")
    with open("files.csv", "w", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer = csv.writer(f)
        # writer = csv.writer(f, quoting=csv.QUOTE_NONE, escapechar="\\")
        writer.writerow(["filename", "year", "term", "exam", "subject_id", "fullpath", "size"])
        total_size = 0

        # Make File objects
        files = [File(file, full_path=os.path.join(all_path, file)) for file in files]

        # Sort files by year, term, exam, and file name
        files.sort(key=lambda x: (x.year, x.term, x.exam, x.name))

        decode = lambda x: x.encode('unicode_escape').decode('latin1').replace(',', '\\,')

        # Write to CSV file and calculate total size
        for file in files:
            row = [file.name, file.year, file.term, file.exam, "|".join(map(str, file.subject_ids)), file.file_path, file.sizestr]
            row[0] = f'"{row[0]}"'
            row[5] = f'"{row[5]}"'
            writer.writerow(row)
            # try:
            # try:
            #     writer.writerow([file.name, file.year, file.term, file.exam, "|".join(map(str, file.subject_ids)), file.file_path, file.sizestr])
            # except UnicodeEncodeError:
            #     writer.writerow([file.name.encode('utf-8'), file.year, file.term, file.exam, "|".join(map(str, file.subject_ids)).encode('utf-8'), file.file_path.encode('utf-8'), file.sizestr])
            writer.writerow([decode(file.name), file.year, file.term, file.exam, "|".join(map(str, file.subject_ids)), decode(file.file_path), file.sizestr])
            
            # try:
            #     writer.writerow([f'"{file.name}"', file.year, file.term, file.exam, "|".join(map(str, file.subject_ids)), f'"{file.file_path}"', file.sizestr])
            # except UnicodeEncodeError:
            #     writer.writerow([f'"{file.name}"'.encode('utf-8'), file.year, file.term, file.exam, "|".join(map(str, file.subject_ids)).encode('utf-8'), f'"{file.file_path}"'.encode('utf-8'), file.sizestr])
            
            # print(file.file_path)
            total_size += file.sizeint

    print(f"Total files: {len(files)}")
    # print(f"Total storage: {total_size:,} Byte ({total_size / 1024 / 1024:.4f} MB)")
    print(f"Total storage: {total_size:,} Byte ({add_size_unit(total_size)})")
    prettify_csv_fixed_width("files.csv", "files.csv")

/*******  d85d2a9a-b3a6-45e0-801f-9a471bfa9b32  *******/
if __name__ == "__main__":
    main()

