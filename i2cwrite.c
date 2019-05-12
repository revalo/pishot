// Written originally by Hermann-SW.
// https://github.com/Hermann-SW

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <unistd.h>

#define I2C_SLAVE_FORCE 0x0706
#define WRITE_I2C(fd, buf, len) (write(fd, buf, len) != len)

int main(int argc, char* argv[]) {
  int i2c_fd = 0;
  char* i2c_device_name;

  assert(argc > 3 && "write dev hex_addr hex_byte1 hex_byte2 ...");
  i2c_device_name = argv[1];

  i2c_fd = open(i2c_device_name, O_RDWR);
  assert(i2c_fd);
  assert(ioctl(i2c_fd, I2C_SLAVE_FORCE, 0x36) >= 0);

  unsigned addr = strtol(argv[2], NULL, 16);
  unsigned len = 2 + argc - 3;
  unsigned i;
  char* buf = malloc(len);

  buf[0] = addr >> 8;
  buf[1] = addr & 0xFF;
  for (i = 3; i < argc; ++i) buf[i - 1] = strtol(argv[i], NULL, 16);

  assert(WRITE_I2C(i2c_fd, buf, len) == 0);
  free(buf);

  if (i2c_fd) close(i2c_fd);

  return 0;
}
