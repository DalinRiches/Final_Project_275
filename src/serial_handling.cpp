#include "serial_handling.h"

#include <Arduino.h>
#include <errno.h>
#include "dprintf.h"

/*
    Function to read a single line from the serial buffer up to a
    specified length (length includes the null termination character
    that must be appended onto the string). This function is blocking.
    The newline character sequence is given by CRLF, or "\r\n".

    Arguments:

    buffer - Pointer to a buffer of characters where the string will
        be stored.

    length - The maximum length of the string to be read.

    Preconditions:  None.

    Postconditions: Function will block until a full newline has been
        read, or the maximum length has been reached. Afterwards the new
        string will be stored in the buffer passed to the function.

    Returns: the number of bytes read

*/
int16_t serial_readline(char *line, uint16_t line_size) {
    int bytes_read = 0;    // Number of bytes read from the serial port.

    // Read until we hit the maximum length, or a newline.
    // One less than the maximum length because we want to add a null terminator.
    while (bytes_read < line_size - 1) {
        while (Serial.available() == 0) {
            // There is no data to be read from the serial port.
            // Wait until data is available.
        }

        line[bytes_read] = (char) Serial.read();

        // A newline is given by \r or \n, or some combination of both
        // or the read may have failed and returned 0
        if ( line[bytes_read] == '\r' || line[bytes_read] == '\n' ||
             line[bytes_read] == 0 ) {
                // We ran into a newline character!  Overwrite it with \0
                break;    // Break out of this - we are done reading a line.
        } else {
            bytes_read++;
        }
    }

    // Add null termination to the end of our string.
    line[bytes_read] = '\0';
    return bytes_read;
    }

/*
    Function to read a portion of a string into a buffer, up to any
    given separation characters. This will read up to the specified
    length of the character buffer if a separation character is not
    encountered, or until the end of the string which is being copied. A
    starting index of the string being copied can also be specified.

    Arguments:

    str -  The string which is having a portion copied.
    str_start -  The index of the string to start at. (Less than str's length).
    buf -  The buffer to store the copied chunk of the string into.
    buf_len -  The length of the buffer.
    sep -  String containing characters that will be used as separators.

    Preconditions:  Make sure str_start does *NOT* exceed the size of str.

    Postconditions: Stores the resulting string in buf, and returns the
    position where reading was left off at.  The position returned will skip
    separation characters.

*/
int16_t string_read_field(const char *str, uint16_t str_start,
    char *field, uint16_t field_size, const char *sep) {

    // Want to read from the string until we encounter the separator.

    // Character that we are reading from the string.
    uint16_t str_index = str_start;

    while (1) {
        if ( str[str_index] == '\0') {
            str_index++;  // signal off end of str
            break;
            }

        if ( field_size <= 1 ) break;

        if (strchr(sep, str[str_index])) {
            // field finished, skip over the separator character.
            str_index++;
            break;
            }

        // Copy the string character into buffer and move over to next
        *field = str[str_index];
        field++;
        field_size--;
        // Move on to the next character.
        str_index++;
        }

    // Make sure to add NULL termination to our new string.
    *field = '\0';

    // Return the index of where the next token begins.
    return str_index;
    }

/*
    Function to convert a string to an int32_t.

    Arguments:
    str -  The string to convert to an integer.

    Preconditions:  The string should probably represent an integer value.

    Postconditions:
        Will return the equivalent integer. If an error occured the
        blink assert may be triggered, and sometimes zero is just
        returned from this function because EINVAL does not exist for
        the Arduino strtol.

 */

int32_t string_get_int(const char *str) {
    // Attempt to convert the string to an integer using strtol...
    int32_t val = strtol(str, NULL, 10);


    return val;
    }
